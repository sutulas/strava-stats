"""
Data merge service for combining new activities with existing data.
This service ensures no duplicates and maintains data integrity.
"""

import pandas as pd
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from services.format_data_service import FormatDataService
from services.supabase_data_service import supabase_data_service

logger = logging.getLogger(__name__)

class DataMergeService:
    """
    Service for merging new activities with existing data.
    Handles deduplication and data integrity.
    """
    
    def __init__(self):
        self.format_service = FormatDataService()
    
    def merge_activities_data(self, user_id: str, new_activities: List[Dict[str, Any]]) -> Optional[pd.DataFrame]:
        """
        Merge new activities with existing data, ensuring no duplicates.
        
        Args:
            user_id: User's Strava ID
            new_activities: List of new activities from Strava API
            
        Returns:
            Combined DataFrame with all activities, or None if error
        """
        try:
            if not new_activities:
                logger.info(f"No new activities to merge for user {user_id}")
                return None
            
            logger.info(f"Merging {len(new_activities)} new activities for user {user_id}")
            
            # Format the new activities
            new_df = self.format_service.format_data(new_activities)
            if new_df.empty:
                logger.warning(f"No running activities found in new data for user {user_id}")
                return None
            
            # Process the new data
            new_df = self.format_service.fix_data(new_df)
            logger.info(f"Formatted {len(new_df)} new running activities")
            
            # Get existing data from Supabase
            existing_df = supabase_data_service.get_user_data(user_id)
            
            if existing_df is None or existing_df.empty:
                logger.info(f"No existing data found for user {user_id}, using only new data")
                return new_df
            
            logger.info(f"Found {len(existing_df)} existing activities for user {user_id}")
            
            # Combine the dataframes
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            
            # Remove duplicates based on activity ID
            initial_count = len(combined_df)
            combined_df = combined_df.drop_duplicates(subset=['id'], keep='first')
            final_count = len(combined_df)
            
            duplicates_removed = initial_count - final_count
            if duplicates_removed > 0:
                logger.info(f"Removed {duplicates_removed} duplicate activities")
            
            # Sort by date (most recent first)
            combined_df['start_date_local'] = pd.to_datetime(combined_df['start_date_local'])
            combined_df = combined_df.sort_values('start_date_local', ascending=False)
            
            logger.info(f"Successfully merged data: {len(existing_df)} existing + {len(new_df)} new = {len(combined_df)} total activities")
            
            return combined_df
            
        except Exception as e:
            logger.error(f"Error merging activities data for user {user_id}: {e}")
            return None
    
    def validate_merged_data(self, df: pd.DataFrame) -> bool:
        """
        Validate the merged data for integrity.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        try:
            if df is None or df.empty:
                logger.warning("DataFrame is empty or None")
                return False
            
            # Check for required columns
            required_columns = ['id', 'start_date_local', 'name', 'distance', 'moving_time']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                logger.error(f"Missing required columns: {missing_columns}")
                return False
            
            # Check for duplicate IDs
            duplicate_ids = df['id'].duplicated().sum()
            if duplicate_ids > 0:
                logger.error(f"Found {duplicate_ids} duplicate activity IDs")
                return False
            
            # Check for valid date range
            try:
                df['start_date_local'] = pd.to_datetime(df['start_date_local'])
                min_date = df['start_date_local'].min()
                max_date = df['start_date_local'].max()
                
                if min_date > max_date:
                    logger.error("Invalid date range: min date is after max date")
                    return False
                
                logger.info(f"Data validation passed. Date range: {min_date} to {max_date}")
                
            except Exception as e:
                logger.error(f"Error validating date range: {e}")
                return False
            
            logger.info(f"Data validation passed for {len(df)} activities")
            return True
            
        except Exception as e:
            logger.error(f"Error validating merged data: {e}")
            return False
    
    def get_merge_summary(self, user_id: str, new_activities_count: int, merged_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get a summary of the merge operation.
        
        Args:
            user_id: User's Strava ID
            new_activities_count: Number of new activities processed
            merged_df: Final merged DataFrame
            
        Returns:
            Dictionary with merge summary information
        """
        try:
            existing_df = supabase_data_service.get_user_data(user_id)
            existing_count = len(existing_df) if existing_df is not None else 0
            
            summary = {
                "user_id": user_id,
                "existing_activities": existing_count,
                "new_activities": new_activities_count,
                "total_activities": len(merged_df),
                "merge_timestamp": datetime.now().isoformat(),
                "data_integrity_valid": self.validate_merged_data(merged_df)
            }
            
            # Add date range information
            if not merged_df.empty:
                merged_df['start_date_local'] = pd.to_datetime(merged_df['start_date_local'])
                summary["date_range"] = {
                    "earliest_activity": merged_df['start_date_local'].min().isoformat(),
                    "latest_activity": merged_df['start_date_local'].max().isoformat()
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating merge summary: {e}")
            return {
                "user_id": user_id,
                "error": str(e),
                "merge_timestamp": datetime.now().isoformat()
            }