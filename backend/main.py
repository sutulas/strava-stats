from fastapi import FastAPI, HTTPException, BackgroundTasks, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
import pandas as pd
from typing import Optional
import uuid
import asyncio
from datetime import datetime
import logging
from pydantic import BaseModel

from routes.analysis import router as analysis_router
from services.chat_workflow import StravaWorkflow
from services.strava_auth_service import StravaAuthService
from services.strava_data_service import StravaDataService
from services.format_data_service import FormatDataService
from services.user_analytics_service import UserAnalyticsService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pydantic models
class TokenRequest(BaseModel):
    code: str

class DataRefreshResponse(BaseModel):
    message: str
    activities_count: int
    file_path: str
    timestamp: str

# Create FastAPI app
app = FastAPI(
    title="Strava Stats API",
    description="A production-ready API for analyzing Strava running data using AI-powered chat workflow",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analysis_router, tags=["analysis"])

# Global workflow instance
workflow = None

@app.on_event("startup")
async def startup_event():
    """Initialize the workflow on startup"""
    global workflow
    try:
        workflow = StravaWorkflow()
        # Set the global workflow instance in the analysis router
        from routes.analysis import workflow as router_workflow
        import routes.analysis
        routes.analysis.workflow = workflow
        logger.info("Strava workflow initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize workflow: {e}")
        raise e

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Strava Stats API is running",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    data_file_exists = os.path.exists("fixed_formatted_run_data.csv")
    
    return {
        "status": "healthy",
        "data_file_exists": data_file_exists,
        "workflow_initialized": workflow is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/auth/token")
async def exchange_token(token_request: TokenRequest):
    """Exchange Strava authorization code for access token"""
    try:
        auth_service = StravaAuthService()
        auth_service.code = token_request.code
        
        # Get the access token
        access_token = auth_service.get_access_token()
        
        # For now, we'll return a simple response
        # In a real implementation, you'd want to store this securely
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_at": None,  # Strava tokens don't expire unless revoked
            "refresh_token": None,  # Strava doesn't provide refresh tokens in this flow
            "scope": "activity:read_all"
        }
    except Exception as e:
        logger.error(f"Token exchange failed: {e}")
        raise HTTPException(status_code=400, detail=f"Token exchange failed: {str(e)}")

@app.post("/data/refresh", response_model=DataRefreshResponse)
async def refresh_user_data(authorization: str = Header(...)):
    """Fetch fresh Strava data and update the workflow dataset"""
    try:
        # Extract token from Authorization header
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        access_token = authorization.replace("Bearer ", "")
        logger.info("Starting data refresh for user")
        
        # Fetch activities from Strava
        strava_service = StravaDataService()
        activities = strava_service.get_activities(access_token)
        
        if not activities:
            logger.warning("No activities found for user")
            raise HTTPException(status_code=404, detail="No activities found")
        
        logger.info(f"Successfully fetched {len(activities)} activities from Strava")
        
        # Format the data
        format_service = FormatDataService()
        formatted_df = format_service.format_data(activities)
        logger.info(f"Formatted {len(formatted_df)} running activities")
        
        # Save formatted data
        formatted_file_path = "data/formatted_data.csv"
        os.makedirs("data", exist_ok=True)
        formatted_df.to_csv(formatted_file_path, index=False)
        logger.info(f"Saved formatted data to {formatted_file_path}")
        
        # Fix and process the data
        format_service.fix_data(formatted_file_path)
        logger.info("Data processing completed successfully")
        
        # Update the workflow with new data
        global workflow
        if workflow:
            try:
                # Reload the workflow with new data
                workflow = StravaWorkflow()
                # Update the router workflow instance
                from routes.analysis import workflow as router_workflow
                import routes.analysis
                routes.analysis.workflow = workflow
                logger.info("Workflow updated with fresh data")
            except Exception as e:
                logger.error(f"Failed to update workflow: {e}")
                # Continue anyway, the data is still processed
        
        return DataRefreshResponse(
            message="Data refreshed successfully",
            activities_count=len(activities),
            file_path="fixed_formatted_run_data.csv",
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Data refresh failed: {e}")
        raise HTTPException(status_code=500, detail=f"Data refresh failed: {str(e)}")

@app.get("/data/status")
async def get_data_status():
    """Get the current status of the user's data"""
    try:
        data_file_exists = os.path.exists("fixed_formatted_run_data.csv")
        formatted_file_exists = os.path.exists("data/formatted_data.csv")
        
        if data_file_exists:
            df = pd.read_csv("fixed_formatted_run_data.csv")
            activities_count = len(df)
            latest_activity = df['start_date_local'].max() if not df.empty else None
        else:
            activities_count = 0
            latest_activity = None
        
        return {
            "data_processed": data_file_exists,
            "formatted_data_exists": formatted_file_exists,
            "activities_count": activities_count,
            "latest_activity": latest_activity,
            "workflow_ready": workflow is not None,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get data status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get data status: {str(e)}")

@app.get("/user/profile")
async def get_user_profile(authorization: str = Header(...)):
    """Get user profile information from Strava"""
    try:
        # Extract token from Authorization header
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        access_token = authorization.replace("Bearer ", "")
        
        # Get user profile
        analytics_service = UserAnalyticsService()
        profile_data = analytics_service.get_user_profile_data(access_token)
        
        if not profile_data:
            raise HTTPException(status_code=404, detail="Failed to fetch user profile")
        
        return profile_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user profile: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get user profile: {str(e)}")

@app.get("/user/stats")
async def get_user_stats(authorization: str = Header(...)):
    """Get comprehensive user statistics and analytics"""
    try:
        # Extract token from Authorization header
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        access_token = authorization.replace("Bearer ", "")
        
        # Get user stats
        analytics_service = UserAnalyticsService()
        stats_data = analytics_service.get_user_stats()
        
        if "error" in stats_data:
            raise HTTPException(status_code=404, detail=stats_data["error"])
        
        return stats_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get user stats: {str(e)}")

@app.get("/user/recent-activities")
async def get_recent_activities(authorization: str = Header(...), limit: int = 10):
    """Get recent running activities"""
    try:
        # Extract token from Authorization header
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        access_token = authorization.replace("Bearer ", "")
        
        # Get recent activities
        analytics_service = UserAnalyticsService()
        activities = analytics_service.get_recent_activities(limit=limit)
        
        return {"activities": activities}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get recent activities: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get recent activities: {str(e)}")

@app.get("/chart.png")
async def get_chart():
    """Serve the generated chart image"""
    if os.path.exists("chart.png"):
        return FileResponse("chart.png", media_type="image/png")
    else:
        raise HTTPException(status_code=404, detail="Chart not found")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 