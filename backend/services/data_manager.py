"""
Centralized data management service for handling processed data across the application.
This ensures data consistency and prevents data loss in production environments.
"""

import pandas as pd
import logging
from typing import Optional, Dict, Any
from datetime import datetime

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
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
        return cls._instance
    
    def set_processed_data(self, data: pd.DataFrame) -> None:
        """Set the processed data and clear caches."""
        self._processed_data = data.copy()  # Make a copy to prevent external modifications
        self._cached_user_stats = None
        self._cached_data_overview = None
        self._data_loaded_at = datetime.now()
        logger.info(f"Data manager updated with {len(data)} rows of processed data")
    
    def get_processed_data(self) -> Optional[pd.DataFrame]:
        """Get the processed data."""
        if self._processed_data is not None:
            logger.debug(f"Data manager returning {len(self._processed_data)} rows of data")
        return self._processed_data
    
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
        logger.debug("User stats cached in data manager")
    
    def get_cached_user_stats(self) -> Optional[Dict[str, Any]]:
        """Get cached user statistics."""
        return self._cached_user_stats
    
    def set_cached_data_overview(self, overview: Dict[str, Any]) -> None:
        """Cache data overview."""
        self._cached_data_overview = overview.copy()
        logger.debug("Data overview cached in data manager")
    
    def get_cached_data_overview(self) -> Optional[Dict[str, Any]]:
        """Get cached data overview."""
        return self._cached_data_overview
    
    def get_data_info(self) -> Dict[str, Any]:
        """Get information about the current data state."""
        return {
            "has_data": self.has_data(),
            "data_rows": len(self._processed_data) if self._processed_data is not None else 0,
            "data_loaded_at": self._data_loaded_at.isoformat() if self._data_loaded_at else None,
            "has_cached_stats": self._cached_user_stats is not None,
            "has_cached_overview": self._cached_data_overview is not None
        }

# Global instance
data_manager = DataManager()