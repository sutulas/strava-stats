from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Header
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import pandas as pd
import os
import logging
import asyncio
from datetime import datetime
import json
import base64

from services.chat_workflow import StravaWorkflow
from services.rate_limiting_service import rate_limiter
from services.data_manager import data_manager
from langchain.schema import HumanMessage

logger = logging.getLogger(__name__)

router = APIRouter()

# Global variable to store chart data for serverless environments
current_chart_data = None

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str = Field(..., description="The user's analysis query", min_length=1, max_length=1000)
    include_chart: bool = Field(default=True, description="Whether to generate a chart for the query")

class QueryResponse(BaseModel):
    query: str
    response: str
    chart_generated: bool
    chart_url: Optional[str] = None
    chart_data: Optional[str] = None  # Base64 encoded chart data
    execution_time: float
    timestamp: str
    status: str

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: str

class RateLimitResponse(BaseModel):
    query_count: int
    remaining_queries: int
    max_queries: int
    session_start: Optional[str] = None
    rate_limited: bool

# Global workflow instance (will be set by main.py)
workflow: Optional[StravaWorkflow] = None

def get_workflow() -> StravaWorkflow:
    """Dependency to get the workflow instance, auto-initializing if needed"""
    global workflow
    
    if workflow is None:
        logger.info("Workflow not initialized, attempting auto-initialization...")
        try:
            # Check for required environment variables
            import os
            openai_key = os.getenv("OPENAI_API_KEY")
            if not openai_key:
                logger.error("OPENAI_API_KEY environment variable is not set")
                raise HTTPException(
                    status_code=503, 
                    detail="Workflow initialization failed: OPENAI_API_KEY environment variable is not set"
                )
            
            # Initialize workflow
            workflow = StravaWorkflow()
            logger.info("Workflow auto-initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to auto-initialize workflow: {e}")
            raise HTTPException(
                status_code=503, 
                detail=f"Workflow initialization failed: {str(e)}"
            )
    
    return workflow

def check_data_file(user_id: str):
    """Check if the required data is available in memory for a specific user"""
    if not data_manager.has_data(user_id):
        raise HTTPException(
            status_code=404, 
            detail="No data available. Please refresh your data first."
        )

@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    authorization: str = Header(...),
    workflow_instance: StravaWorkflow = Depends(get_workflow)
):
    """
    Process a user query using the Strava chat workflow.
    
    This endpoint takes a natural language query about running data and returns
    an analysis response, optionally generating a chart.
    """
    start_time = datetime.now()
    
    try:
        # Extract access token from authorization header
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header format")
        
        access_token = authorization.replace("Bearer ", "")
        
        if not access_token:
            raise HTTPException(status_code=401, detail="No access token provided")
        
        # Check rate limit
        if not rate_limiter.record_query(access_token):
            remaining = rate_limiter.get_remaining_queries(access_token)
            raise HTTPException(
                status_code=429, 
                detail=f"Rate limit exceeded. You have used all {rate_limiter.max_queries} queries for this session."
            )
        
        # Extract user_id from authorization token
        from services.strava_data_service import StravaDataService
        strava_service = StravaDataService()
        user_profile = strava_service.get_user_profile(access_token)
        user_id = str(user_profile['id']) if user_profile else "unknown_user"
        
        # Check if data is available for this user
        check_data_file(user_id)
        
        logger.info(f"Processing query: {request.query}")
        
        # Use the in-memory data from data manager
        df = data_manager.get_processed_data(user_id)
        logger.info(f"Using data with {len(df)} rows")
        
        # Run the workflow
        result = workflow_instance.run_workflow(
            messages=[HumanMessage(content=request.query)], 
            df=df
        )
        
        # Determine response based on workflow result
        global current_chart_data
        if result["chart_generated"]:
            # Chart was generated - trust the workflow's decision
            response_text = result["response"] if result["response"] else "View the chart below."
            chart_generated = True
            # Store the chart data globally for serverless environments
            # The workflow should have stored base64 chart data in chart_output
            current_chart_data = result.get("chart_output")
            chart_url = "/chart"  # Keep for backward compatibility
            chart_data = result.get("chart_output")  # Pass base64 data directly
        elif result["response"]:
            # Data analysis was performed
            response_text = result["response"]
            chart_generated = False
            chart_url = None
            chart_data = None
            current_chart_data = None  # Clear any previous chart data
        else:
            # Fallback response
            response_text = "Analysis completed but no specific output was generated."
            chart_generated = False
            chart_url = None
            chart_data = None
            current_chart_data = None  # Clear any previous chart data
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"Query processed successfully in {execution_time:.2f} seconds")
        
        return QueryResponse(
            query=request.query,
            response=response_text,
            chart_generated=chart_generated,
            chart_url=chart_url,
            chart_data=chart_data,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat(),
            status="success"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        execution_time = (datetime.now() - start_time).total_seconds()
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/chart")
async def get_chart():
    """
    Get the most recently generated chart.
    
    Returns the chart image if it exists, otherwise returns a 404 error.
    """
    global current_chart_data
    
    # First try to serve from global chart data (for serverless environments)
    if current_chart_data and not current_chart_data.startswith("Chart generation failed"):
        try:
            chart_bytes = base64.b64decode(current_chart_data)
            return Response(
                content=chart_bytes,
                media_type="image/png",
                headers={"Cache-Control": "no-cache"}
            )
        except Exception as e:
            logger.error(f"Error serving chart from global data: {e}")
    
    # Fallback to file system (for local development)
    if os.path.exists("chart.png"):
        return FileResponse(
            "chart.png", 
            media_type="image/png",
            headers={"Cache-Control": "no-cache"}
        )
    else:
        raise HTTPException(
            status_code=404, 
            detail="No chart available. Please run a query that generates a chart first."
        )

@router.get("/data/overview")
async def get_data_overview(authorization: str = Header(...)):
    """
    Get an overview of the available data.
    
    Returns basic statistics and information about the loaded dataset.
    """
    try:
        # Extract access token from authorization header
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header format")
        
        access_token = authorization.replace("Bearer ", "")
        
        if not access_token:
            raise HTTPException(status_code=401, detail="No access token provided")
        
        # Extract user_id from authorization token
        from services.strava_data_service import StravaDataService
        strava_service = StravaDataService()
        user_profile = strava_service.get_user_profile(access_token)
        user_id = str(user_profile['id']) if user_profile else "unknown_user"
        
        # Return cached data if available
        cached_overview = data_manager.get_cached_data_overview(user_id)
        if cached_overview is not None:
            logger.info("Returning cached data overview")
            return cached_overview
        
        # Get processed data for the specific user
        df = data_manager.get_processed_data(user_id)
        if df is None:
            raise HTTPException(
                status_code=404, 
                detail="No data available. Please refresh your data first."
            )
        
        overview = {
            "total_activities": len(df),
            "date_range": {
                "start": df['start_date'].min() if 'start_date' in df.columns else None,
                "end": df['start_date'].max() if 'start_date' in df.columns else None
            },
            "columns": list(df.columns),
            "sample_data": df.head(3).to_dict('records'),
            "data_loaded_at": datetime.now().isoformat()
        }
        
        # Cache the results
        data_manager.set_cached_data_overview(overview, user_id)
        logger.info("Cached data overview for future requests")
        
        return overview
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting data overview: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving data overview: {str(e)}"
        )

@router.get("/rate-limit", response_model=RateLimitResponse)
async def get_rate_limit_status(authorization: str = Header(...)):
    """
    Get the current rate limit status for the user.
    
    Returns information about how many queries the user has made and how many remain.
    """
    try:
        # Extract access token from authorization header
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header format")
        
        access_token = authorization.replace("Bearer ", "")
        
        if not access_token:
            raise HTTPException(status_code=401, detail="No access token provided")
        
        # Get rate limit info
        session_info = rate_limiter.get_session_info(access_token)
        
        return RateLimitResponse(**session_info)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting rate limit status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving rate limit status: {str(e)}"
        )

@router.get("/examples")
async def get_example_queries():
    """
    Get example queries that users can try.
    
    Returns a list of example queries to help users understand what they can ask.
    """
    examples = [
        {
            "category": "Basic Statistics",
            "queries": [
                "What is my average running pace?",
                "How many miles have I run this year?",
                "What is my fastest run?",
                "Show me my total elevation gain"
            ]
        },
        {
            "category": "Trends and Analysis",
            "queries": [
                "How has my pace improved over time?",
                "What days of the week do I run most?",
                "Show me my weekly mileage trends",
                "What is my average heart rate during runs?"
            ]
        },
        {
            "category": "Charts and Visualizations",
            "queries": [
                "Create a chart showing my distance over time",
                "Show me a histogram of my running paces",
                "Generate a scatter plot of pace vs heart rate",
                "Create a bar chart of my monthly mileage"
            ]
        }
    ]
    
    return {"examples": examples}
