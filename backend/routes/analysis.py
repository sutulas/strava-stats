from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Header
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import pandas as pd
import os
import logging
import asyncio
from datetime import datetime
import json

from services.chat_workflow import StravaWorkflow
from services.rate_limiting_service import rate_limiter
from langchain.schema import HumanMessage

logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str = Field(..., description="The user's analysis query", min_length=1, max_length=1000)
    include_chart: bool = Field(default=True, description="Whether to generate a chart for the query")

class QueryResponse(BaseModel):
    query: str
    response: str
    chart_generated: bool
    chart_url: Optional[str] = None
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

def check_data_file():
    """Check if the required data file exists"""
    if not os.path.exists("fixed_formatted_run_data.csv"):
        raise HTTPException(
            status_code=404, 
            detail="Data file 'fixed_formatted_run_data.csv' not found. Please ensure the data file is available."
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
        
        # Check if data file exists
        check_data_file()
        
        logger.info(f"Processing query: {request.query}")
        
        # Load the data
        df = pd.read_csv("fixed_formatted_run_data.csv")
        logger.info(f"Loaded data with {len(df)} rows")
        
        # Run the workflow
        result = workflow_instance.run_workflow(
            messages=[HumanMessage(content=request.query)], 
            df=df
        )
        
        # Determine response based on workflow result
        if result["chart_generated"]:
            # Chart was generated
            response_text = f"View the chart below."
            chart_generated = True
            chart_url = "/chart.png" if os.path.exists("chart.png") else None
        elif result["response"]:
            # Data analysis was performed
            response_text = result["response"]
            chart_generated = False
            chart_url = None
        else:
            # Fallback response
            response_text = "Analysis completed but no specific output was generated."
            chart_generated = False
            chart_url = None
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"Query processed successfully in {execution_time:.2f} seconds")
        
        return QueryResponse(
            query=request.query,
            response=response_text,
            chart_generated=chart_generated,
            chart_url=chart_url,
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
async def get_data_overview():
    """
    Get an overview of the available data.
    
    Returns basic statistics and information about the loaded dataset.
    """
    try:
        check_data_file()
        
        df = pd.read_csv("fixed_formatted_run_data.csv")
        
        overview = {
            "total_activities": len(df),
            "date_range": {
                "start": df['start_date'].min() if 'start_date' in df.columns else None,
                "end": df['start_date'].max() if 'start_date' in df.columns else None
            },
            "activity_types": df['type'].value_counts().to_dict() if 'type' in df.columns else {},
            "columns": list(df.columns),
            "sample_data": df.head(3).to_dict('records'),
            "data_loaded_at": datetime.now().isoformat()
        }
        
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
