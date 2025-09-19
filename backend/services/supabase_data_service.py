"""
Supabase data service for persistent data storage.
This provides a reliable alternative to in-memory storage for production.
"""

import pandas as pd
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import os
from supabase import create_client, Client

logger = logging.getLogger(__name__)

class SupabaseDataService:
    """
    Data service using Supabase for persistent storage.
    Falls back to in-memory storage if Supabase is not configured.
    """
    
    def __init__(self):
        self.supabase: Optional[Client] = None
        self.use_supabase = False
        
        # Try to initialize Supabase
        try:
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_ANON_KEY")
            
            if supabase_url and supabase_key:
                self.supabase = create_client(supabase_url, supabase_key)
                self.use_supabase = True
                logger.info("Supabase data service initialized successfully")
            else:
                logger.warning("Supabase credentials not found, using in-memory fallback")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase: {e}")
            logger.warning("Falling back to in-memory storage")
    
    def store_user_data(self, user_id: str, data: pd.DataFrame) -> bool:
        """Store user's processed data in Supabase."""
        logger.info(f"Attempting to store data for user {user_id}, Supabase available: {self.use_supabase}")
        
        if not self.use_supabase:
            logger.warning("Supabase not available, data not persisted")
            return False
        
        try:
            # Convert DataFrame to JSON for storage
            data_json = data.to_json(orient='records', date_format='iso')
            logger.info(f"Converted DataFrame to JSON, size: {len(data_json)} characters")
            
            # Store in Supabase
            result = self.supabase.table("user_data").upsert({
                "user_id": user_id,
                "data": data_json,
                "data_type": "processed_activities",
                "row_count": len(data),
                "updated_at": datetime.now().isoformat()
            }).execute()
            
            logger.info(f"Successfully stored {len(data)} rows for user {user_id}")
            logger.info(f"Supabase response: {result}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store user data: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            return False
    
    def get_user_data(self, user_id: str) -> Optional[pd.DataFrame]:
        """Retrieve user's processed data from Supabase."""
        if not self.use_supabase:
            logger.warning("Supabase not available, cannot retrieve data")
            return None
        
        try:
            result = self.supabase.table("user_data").select("*").eq("user_id", user_id).execute()
            
            if result.data:
                data_json = result.data[0]["data"]
                df = pd.read_json(data_json, orient='records')
                logger.info(f"Retrieved {len(df)} rows for user {user_id}")
                return df
            else:
                logger.info(f"No data found for user {user_id}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to retrieve user data: {e}")
            return None
    
    def store_cached_stats(self, user_id: str, stats: Dict[str, Any]) -> bool:
        """Store cached user statistics."""
        if not self.use_supabase:
            return False
        
        try:
            result = self.supabase.table("user_cache").upsert({
                "user_id": user_id,
                "cache_type": "user_stats",
                "cache_data": json.dumps(stats),
                "updated_at": datetime.now().isoformat()
            }).execute()
            
            logger.debug(f"Cached stats for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cache stats: {e}")
            return False
    
    def get_cached_stats(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached user statistics."""
        if not self.use_supabase:
            return None
        
        try:
            result = self.supabase.table("user_cache").select("*").eq("user_id", user_id).eq("cache_type", "user_stats").execute()
            
            if result.data:
                cache_data = json.loads(result.data[0]["cache_data"])
                logger.debug(f"Retrieved cached stats for user {user_id}")
                return cache_data
            else:
                return None
                
        except Exception as e:
            logger.error(f"Failed to retrieve cached stats: {e}")
            return None
    
    def store_cached_overview(self, user_id: str, overview: Dict[str, Any]) -> bool:
        """Store cached data overview."""
        if not self.use_supabase:
            return False
        
        try:
            result = self.supabase.table("user_cache").upsert({
                "user_id": user_id,
                "cache_type": "data_overview",
                "cache_data": json.dumps(overview),
                "updated_at": datetime.now().isoformat()
            }).execute()
            
            logger.debug(f"Cached overview for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cache overview: {e}")
            return False
    
    def get_cached_overview(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached data overview."""
        if not self.use_supabase:
            return None
        
        try:
            result = self.supabase.table("user_cache").select("*").eq("user_id", user_id).eq("cache_type", "data_overview").execute()
            
            if result.data:
                cache_data = json.loads(result.data[0]["cache_data"])
                logger.debug(f"Retrieved cached overview for user {user_id}")
                return cache_data
            else:
                return None
                
        except Exception as e:
            logger.error(f"Failed to retrieve cached overview: {e}")
            return None
    
    def clear_user_data(self, user_id: str) -> bool:
        """Clear all user data and cache."""
        if not self.use_supabase:
            return False
        
        try:
            # Clear user data
            self.supabase.table("user_data").delete().eq("user_id", user_id).execute()
            
            # Clear user cache
            self.supabase.table("user_cache").delete().eq("user_id", user_id).execute()
            
            logger.info(f"Cleared all data for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to clear user data: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if Supabase service is available."""
        return self.use_supabase

# Global instance
supabase_data_service = SupabaseDataService()