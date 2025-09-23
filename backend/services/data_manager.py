"""
Centralized data management service for handling processed data across the application.
This ensures data consistency and prevents data loss in production environments.
"""

import pandas as pd
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from .supabase_data_service import supabase_data_service
from .incremental_data_service import IncrementalDataService
from .data_merge_service import DataMergeService

logger = logging.getLogger(__name__)

class DataManager:
    """
    Centralized data manager that handles all data operations.
    This singleton ensures data consistency across all modules.
    """
    
    _instance = None
    _processed_data: Optional[pd.DataFrame] = None
    _cached_user_stats: Optional[Dict[str, Any]] = None
    _cached_data_overview: Optional[Dict[str, Any]] = None
    _data_loaded_at: Optional[datetime] = None
    _current_user_id: Optional[str] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.incremental_service = IncrementalDataService()
            self.merge_service = DataMergeService()
            self._initialized = True
    
    def set_current_user(self, user_id: str) -> None:
        """Set the current user ID for data operations."""
        self._current_user_id = user_id
        logger.info(f"Data manager set for user: {user_id}")
    
    def set_processed_data(self, data: pd.DataFrame, user_id: Optional[str] = None) -> None:
        """Set the processed data and clear caches."""
        if user_id:
            self.set_current_user(user_id)
        
        logger.info(f"Data manager setting processed data: {len(data)} rows for user {self._current_user_id}")
        
        self._processed_data = data.copy()  # Make a copy to prevent external modifications
        self._cached_user_stats = None
        self._cached_data_overview = None
        self._data_loaded_at = datetime.now()
        
        # Try to persist to Supabase
        if self._current_user_id and supabase_data_service.is_available():
            logger.info(f"Attempting to persist data to Supabase for user {self._current_user_id}")
            success = supabase_data_service.store_user_data(self._current_user_id, data)
            logger.info(f"Supabase persistence result: {success}")
        else:
            logger.info(f"Not persisting to Supabase - user_id: {self._current_user_id}, available: {supabase_data_service.is_available()}")
        
        logger.info(f"Data manager updated with {len(data)} rows of processed data")
    
    def get_processed_data(self, user_id: Optional[str] = None) -> Optional[pd.DataFrame]:
        """Get the processed data."""
        if user_id:
            self.set_current_user(user_id)
        
        # If we have data in memory, return it
        if self._processed_data is not None:
            logger.debug(f"Data manager returning {len(self._processed_data)} rows of data from memory")
            return self._processed_data
        
        # Try to load from Supabase if available
        if self._current_user_id and supabase_data_service.is_available():
            data = supabase_data_service.get_user_data(self._current_user_id)
            if data is not None:
                self._processed_data = data
                self._data_loaded_at = datetime.now()
                logger.info(f"Loaded {len(data)} rows from Supabase for user {self._current_user_id}")
                return data
        
        logger.debug("No data available in memory or Supabase")
        return None
    
    def has_data(self) -> bool:
        """Check if processed data is available."""
        return self._processed_data is not None and not self._processed_data.empty
    
    def clear_data(self) -> None:
        """Clear all data and caches."""
        self._processed_data = None
        self._cached_user_stats = None
        self._cached_data_overview = None
        self._data_loaded_at = None
        logger.info("Data manager cleared all data")
    
    def set_cached_user_stats(self, stats: Dict[str, Any]) -> None:
        """Cache user statistics."""
        self._cached_user_stats = stats.copy()
        
        # Try to persist to Supabase
        if self._current_user_id and supabase_data_service.is_available():
            supabase_data_service.store_cached_stats(self._current_user_id, stats)
        
        logger.debug("User stats cached in data manager")
    
    def get_cached_user_stats(self) -> Optional[Dict[str, Any]]:
        """Get cached user statistics."""
        # Return from memory if available
        if self._cached_user_stats is not None:
            return self._cached_user_stats
        
        # Try to load from Supabase
        if self._current_user_id and supabase_data_service.is_available():
            stats = supabase_data_service.get_cached_stats(self._current_user_id)
            if stats is not None:
                self._cached_user_stats = stats
                return stats
        
        return None
    
    def set_cached_data_overview(self, overview: Dict[str, Any]) -> None:
        """Cache data overview."""
        self._cached_data_overview = overview.copy()
        
        # Try to persist to Supabase
        if self._current_user_id and supabase_data_service.is_available():
            supabase_data_service.store_cached_overview(self._current_user_id, overview)
        
        logger.debug("Data overview cached in data manager")
    
    def get_cached_data_overview(self) -> Optional[Dict[str, Any]]:
        """Get cached data overview."""
        # Return from memory if available
        if self._cached_data_overview is not None:
            return self._cached_data_overview
        
        # Try to load from Supabase
        if self._current_user_id and supabase_data_service.is_available():
            overview = supabase_data_service.get_cached_overview(self._current_user_id)
            if overview is not None:
                self._cached_data_overview = overview
                return overview
        
        return None
    
    def clear_data(self) -> None:
        """Clear all data and caches."""
        self._processed_data = None
        self._cached_user_stats = None
        self._cached_data_overview = None
        self._data_loaded_at = None
        
        # Clear from Supabase if available
        if self._current_user_id and supabase_data_service.is_available():
            supabase_data_service.clear_user_data(self._current_user_id)
        
        logger.info("Data manager cleared all data")
    
    def get_data_info(self) -> Dict[str, Any]:
        """Get information about the current data state."""
        return {
            "has_data": self.has_data(),
            "data_rows": len(self._processed_data) if self._processed_data is not None else 0,
            "data_loaded_at": self._data_loaded_at.isoformat() if self._data_loaded_at else None,
            "has_cached_stats": self._cached_user_stats is not None,
            "has_cached_overview": self._cached_data_overview is not None,
            "supabase_available": supabase_data_service.is_available(),
            "current_user": self._current_user_id
        }
    
    def load_user_data_incremental(self, access_token: str, user_id: str) -> Dict[str, Any]:
        """
        Load user data using incremental approach - only fetch new activities.
        
        Args:
            access_token: Strava access token
            user_id: User's Strava ID
            
        Returns:
            Dictionary with loading results and summary
        """
        try:
            logger.info(f"Starting incremental data load for user {user_id}")
            
            # Determine fetch strategy
            fetch_strategy = self.incremental_service.get_data_fetch_strategy(user_id)
            logger.info(f"Using {fetch_strategy} fetch strategy for user {user_id}")
            
            # Fetch new activities
            new_activities = self.incremental_service.fetch_new_activities(access_token, user_id)
            
            if not new_activities:
                logger.info(f"No new activities found for user {user_id}")
                return {
                    "success": True,
                    "strategy": fetch_strategy,
                    "new_activities": 0,
                    "total_activities": len(self._processed_data) if self._processed_data is not None else 0,
                    "message": "No new activities found"
                }
            
            # Merge new activities with existing data
            merged_df = self.merge_service.merge_activities_data(user_id, new_activities)
            
            if merged_df is None:
                logger.error(f"Failed to merge data for user {user_id}")
                return {
                    "success": False,
                    "strategy": fetch_strategy,
                    "error": "Failed to merge new activities with existing data"
                }
            
            # Validate merged data
            if not self.merge_service.validate_merged_data(merged_df):
                logger.error(f"Data validation failed for user {user_id}")
                return {
                    "success": False,
                    "strategy": fetch_strategy,
                    "error": "Data validation failed"
                }
            
            # Store the merged data
            self.set_processed_data(merged_df, user_id)
            
            # Get merge summary
            merge_summary = self.merge_service.get_merge_summary(user_id, len(new_activities), merged_df)
            
            logger.info(f"Incremental data load completed for user {user_id}: {len(new_activities)} new activities")
            
            return {
                "success": True,
                "strategy": fetch_strategy,
                "new_activities": len(new_activities),
                "total_activities": len(merged_df),
                "merge_summary": merge_summary,
                "message": f"Successfully loaded {len(new_activities)} new activities"
            }
            
        except Exception as e:
            logger.error(f"Error in incremental data load for user {user_id}: {e}")
            return {
                "success": False,
                "strategy": "incremental",
                "error": str(e)
            }
    
    def check_data_freshness(self, user_id: str) -> Dict[str, Any]:
        """
        Check how fresh the user's data is.
        
        Args:
            user_id: User's Strava ID
            
        Returns:
            Dictionary with freshness information
        """
        try:
            # Get metadata from Supabase
            metadata = supabase_data_service.get_user_data_metadata(user_id)
            
            if metadata is None:
                return {
                    "has_data": False,
                    "last_updated": None,
                    "data_age_hours": None,
                    "needs_refresh": True
                }
            
            # Calculate data age
            last_updated = datetime.fromisoformat(metadata["updated_at"])
            data_age_hours = (datetime.now() - last_updated).total_seconds() / 3600
            
            # Consider data stale if older than 24 hours
            needs_refresh = data_age_hours > 24
            
            return {
                "has_data": True,
                "last_updated": metadata["updated_at"],
                "data_age_hours": round(data_age_hours, 2),
                "needs_refresh": needs_refresh,
                "row_count": metadata.get("row_count", 0)
            }
            
        except Exception as e:
            logger.error(f"Error checking data freshness for user {user_id}: {e}")
            return {
                "has_data": False,
                "error": str(e),
                "needs_refresh": True
            }

# Global instance
data_manager = DataManager()