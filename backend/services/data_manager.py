"""
Centralized data management service for handling processed data across the application.
This ensures data consistency and prevents data loss in production environments.
"""

import pandas as pd
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from .supabase_data_service import supabase_data_service

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

# Global instance
data_manager = DataManager()