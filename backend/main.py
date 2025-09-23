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
from services.data_manager import data_manager

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
    title="Running Stats API",
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
data_refresh_in_progress = False  # Flag to prevent multiple simultaneous refreshes

async def initialize_workflow_with_retry():
    """Initialize workflow with retry mechanism"""
    global workflow
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Workflow initialization attempt {attempt + 1}/{max_retries}")
            
            # Check for required environment variables
            openai_key = os.getenv("OPENAI_API_KEY")
            if not openai_key:
                logger.error("OPENAI_API_KEY environment variable is not set")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                    continue
                else:
                    logger.warning("Workflow initialization skipped due to missing environment variables")
                    return False
            
            logger.info("Environment variables validated")
            
            # Initialize workflow
            workflow = StravaWorkflow()
            logger.info("StravaWorkflow instance created successfully")
            
            # Set the global workflow instance in the analysis router
            import routes.analysis
            routes.analysis.workflow = workflow
            logger.info("Workflow instance set in analysis router")
            
            logger.info("Strava workflow initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize workflow (attempt {attempt + 1}): {e}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error("All workflow initialization attempts failed")
                return False
    
    return False

@app.on_event("startup")
async def startup_event():
    """Initialize the workflow on startup with retry mechanism"""
    logger.info("Starting workflow initialization...")
    
    # Try immediate initialization
    success = await initialize_workflow_with_retry()
    
    if not success:
        logger.warning("Immediate workflow initialization failed, scheduling delayed initialization")
        # Schedule delayed initialization as background task
        asyncio.create_task(delayed_workflow_initialization())

async def delayed_workflow_initialization():
    """Delayed workflow initialization as fallback"""
    logger.info("Starting delayed workflow initialization...")
    await asyncio.sleep(5)  # Wait 5 seconds
    
    success = await initialize_workflow_with_retry()
    if success:
        logger.info("Delayed workflow initialization successful")
    else:
        logger.error("Delayed workflow initialization also failed")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Running Stats API is running",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    data_info = data_manager.get_data_info()
    data_file_exists = data_info["has_data"]
    
    # Check environment variables
    openai_key_set = bool(os.getenv("OPENAI_API_KEY"))
    
    # Check if workflow is properly initialized (or can be auto-initialized)
    workflow_initialized = workflow is not None
    workflow_can_auto_init = bool(os.getenv("OPENAI_API_KEY"))
    
    # Additional diagnostic info
    diagnostic_info = {
        "environment_variables": {
            "OPENAI_API_KEY_set": openai_key_set
        },
        "files": {
            "data_file_exists": data_file_exists,
            "current_directory": os.getcwd(),
            "files_in_directory": os.listdir(".") if os.path.exists(".") else []
        }
    }
    
    return {
        "status": "healthy",
        "data_file_exists": data_file_exists,
        "workflow_initialized": workflow_initialized,
        "workflow_can_auto_init": workflow_can_auto_init,
        "diagnostic_info": diagnostic_info,
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
    """Fetch fresh Strava data and update the workflow dataset using incremental loading"""
    global data_refresh_in_progress
    
    # Check if refresh is already in progress
    if data_refresh_in_progress:
        logger.info("Data refresh already in progress, skipping duplicate request")
        return DataRefreshResponse(
            message="Data refresh already in progress",
            activities_count=0,
            file_path="in_memory_data",
            timestamp=datetime.now().isoformat()
        )
    
    try:
        data_refresh_in_progress = True
        
        # Extract token from Authorization header
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        access_token = authorization.replace("Bearer ", "")
        logger.info("Starting incremental data refresh for user")
        
        # Get user profile to extract user_id
        strava_service = StravaDataService()
        user_profile = strava_service.get_user_profile(access_token)
        user_id = str(user_profile['id']) if user_profile else "unknown_user"
        
        # Check data freshness first
        freshness_info = data_manager.check_data_freshness(user_id)
        logger.info(f"Data freshness check: {freshness_info}")
        
        # Use incremental loading
        load_result = data_manager.load_user_data_incremental(access_token, user_id)
        
        if not load_result["success"]:
            logger.error(f"Incremental load failed: {load_result.get('error', 'Unknown error')}")
            raise HTTPException(status_code=500, detail=f"Data refresh failed: {load_result.get('error', 'Unknown error')}")
        
        # Get the updated data
        processed_df = data_manager.get_processed_data(user_id)
        
        if processed_df is None or processed_df.empty:
            logger.warning("No data available after refresh")
            raise HTTPException(status_code=404, detail="No data available after refresh")
        
        # Update the workflow with new data
        global workflow
        try:
            # Reload the workflow with new data
            workflow = StravaWorkflow(processed_df)
            # Update the router workflow instance
            import routes.analysis
            routes.analysis.workflow = workflow
            logger.info("Workflow updated with fresh data")
        except Exception as e:
            logger.error(f"Failed to update workflow: {e}")
            # Continue anyway, the data is still processed
        
        return DataRefreshResponse(
            message=f"Data refreshed successfully using {load_result['strategy']} strategy",
            activities_count=load_result["total_activities"],
            file_path="in_memory_data",
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        data_refresh_in_progress = False
        raise
    except Exception as e:
        logger.error(f"Data refresh failed: {e}")
        data_refresh_in_progress = False
        raise HTTPException(status_code=500, detail=f"Data refresh failed: {str(e)}")
    finally:
        data_refresh_in_progress = False

@app.get("/data/freshness")
async def check_data_freshness(authorization: str = Header(...)):
    """Check how fresh the user's data is and whether it needs updating"""
    try:
        # Extract token from Authorization header
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        access_token = authorization.replace("Bearer ", "")
        
        # Get user profile to extract user_id
        strava_service = StravaDataService()
        user_profile = strava_service.get_user_profile(access_token)
        user_id = str(user_profile['id']) if user_profile else "unknown_user"
        
        # Check data freshness
        freshness_info = data_manager.check_data_freshness(user_id)
        
        return freshness_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to check data freshness: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to check data freshness: {str(e)}")

@app.get("/data/status")
async def get_data_status():
    """Get the current status of the user's data"""
    try:
        data_info = data_manager.get_data_info()
        
        if data_info["has_data"]:
            activities_count = data_info["data_rows"]
            latest_activity = None  # We could add this to the data manager if needed
        else:
            activities_count = 0
            latest_activity = None
        
        return {
            "data_processed": data_info["has_data"],
            "formatted_data_exists": data_info["has_data"],
            "activities_count": activities_count,
            "latest_activity": latest_activity,
            "workflow_ready": workflow is not None,
            "data_loaded_at": data_info["data_loaded_at"],
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
            raise HTTPException(status_code=401, detail="Invalid authorization header format")
        
        access_token = authorization.replace("Bearer ", "")
        
        if not access_token:
            raise HTTPException(status_code=401, detail="No access token provided")
        
        # Get user profile
        analytics_service = UserAnalyticsService()
        profile_data = analytics_service.get_user_profile_data(access_token)
        
        return profile_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user profile: {e}")
        # Check if it's a Strava API authentication error
        if "401" in str(e) or "Unauthorized" in str(e):
            raise HTTPException(status_code=401, detail="Invalid or expired Strava access token")
        elif "Network error" in str(e):
            raise HTTPException(status_code=503, detail="Unable to connect to Strava API")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to get user profile: {str(e)}")

@app.get("/user/stats")
async def get_user_stats(authorization: str = Header(...)):
    """Get comprehensive user statistics and analytics"""
    try:
        # Extract token from Authorization header
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        access_token = authorization.replace("Bearer ", "")
        
        # Get user profile to extract user_id
        strava_service = StravaDataService()
        user_profile = strava_service.get_user_profile(access_token)
        user_id = str(user_profile['id']) if user_profile else "unknown_user"
        
        # Return cached data if available
        cached_stats = data_manager.get_cached_user_stats()
        if cached_stats is not None:
            logger.info("Returning cached user stats")
            return cached_stats
        
        # Get processed data from data manager
        processed_data = data_manager.get_processed_data(user_id)
        if processed_data is None:
            raise HTTPException(status_code=404, detail="No data available. Please refresh your data first.")
        
        # Get user stats
        analytics_service = UserAnalyticsService()
        stats_data = analytics_service.get_user_stats(processed_data)
        
        if "error" in stats_data:
            raise HTTPException(status_code=404, detail=stats_data["error"])
        
        # Cache the results
        data_manager.set_cached_user_stats(stats_data)
        logger.info("Cached user stats for future requests")
        
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
        
        # Get user profile to extract user_id
        strava_service = StravaDataService()
        user_profile = strava_service.get_user_profile(access_token)
        user_id = str(user_profile['id']) if user_profile else "unknown_user"
        
        # Get processed data from data manager
        processed_data = data_manager.get_processed_data(user_id)
        if processed_data is None:
            raise HTTPException(status_code=404, detail="No data available. Please refresh your data first.")
        
        # Get recent activities
        analytics_service = UserAnalyticsService()
        activities = analytics_service.get_recent_activities(processed_data, limit=limit)
        
        return {"activities": activities}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get recent activities: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get recent activities: {str(e)}")

@app.post("/admin/initialize-workflow")
async def manual_workflow_initialization():
    """Manually initialize the workflow (admin endpoint)"""
    logger.info("Manual workflow initialization requested...")
    
    success = await initialize_workflow_with_retry()
    
    if success:
        return {
            "success": True,
            "message": "Workflow initialized successfully",
            "timestamp": datetime.now().isoformat()
        }
    else:
        return {
            "success": False,
            "error": "Workflow initialization failed after all retry attempts",
            "timestamp": datetime.now().isoformat()
        }

@app.delete("/data/delete")
async def delete_user_data(authorization: str = Header(...)):
    """Delete all user data and revoke Strava access"""
    try:
        # Extract token from Authorization header
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        access_token = authorization.replace("Bearer ", "")
        logger.info("User data deletion requested")
        
        # Get user profile to extract user_id for Supabase cleanup
        strava_service = StravaDataService()
        user_profile = strava_service.get_user_profile(access_token)
        user_id = str(user_profile['id']) if user_profile else "unknown_user"
        
        logger.info(f"Deleting data for user: {user_id}")
        
        # Clear all data using centralized data manager (this will also clear Supabase)
        data_manager.clear_data()
        
        # Clear workflow
        global workflow
        workflow = None
        
        # List of files to delete (if they exist)
        files_to_delete = [
            "data/formatted_data.csv",
            "chart.png"
        ]
        
        deleted_files = []
        errors = []
        
        # Delete data files
        for file_path in files_to_delete:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_files.append(file_path)
                    logger.info(f"Deleted file: {file_path}")
            except Exception as e:
                error_msg = f"Failed to delete {file_path}: {str(e)}"
                errors.append(error_msg)
                logger.error(error_msg)
        
        # Clean up data directory if empty
        try:
            if os.path.exists("data") and not os.listdir("data"):
                os.rmdir("data")
                deleted_files.append("data/")
                logger.info("Removed empty data directory")
        except Exception as e:
            error_msg = f"Failed to remove data directory: {str(e)}"
            errors.append(error_msg)
            logger.error(error_msg)
        
        # Reset workflow to clear any cached data
        if workflow:
            try:
                workflow = None
                logger.info("Workflow instance cleared")
            except Exception as e:
                error_msg = f"Failed to clear workflow: {str(e)}"
                errors.append(error_msg)
                logger.error(error_msg)
        
        # Prepare response
        response = {
            "message": "User data deletion completed (including Supabase data)",
            "user_id": user_id,
            "deleted_files": deleted_files,
            "timestamp": datetime.now().isoformat()
        }
        
        if errors:
            response["warnings"] = errors
        
        logger.info(f"Data deletion completed. Files deleted: {len(deleted_files)}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete user data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete user data: {str(e)}")

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