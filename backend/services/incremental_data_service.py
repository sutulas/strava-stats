"""
Incremental data service for fetching only new activities since last update.
This service optimizes data loading by only fetching activities newer than the last stored data.
"""

import pandas as pd
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
import requests
from services.strava_data_service import StravaDataService
from services.format_data_service import FormatDataService
from services.supabase_data_service import supabase_data_service

logger = logging.getLogger(__name__)

class IncrementalDataService:
    """
    Service for incremental data loading from Strava API.
    Only fetches activities newer than the last stored data.
    """
    
    def __init__(self):
        self.strava_service = StravaDataService()
        self.format_service = FormatDataService()
    
    def get_last_activity_date(self, user_id: str) -> Optional[datetime]:
        """
        Get the date of the most recent activity stored in the database.
        
        Args:
            user_id: The user's Strava ID
            
        Returns:
            datetime of the most recent activity, or None if no data exists
        """
        try:
            # Get existing data from Supabase
            existing_data = supabase_data_service.get_user_data(user_id)
            
            if existing_data is None or existing_data.empty:
                logger.info(f"No existing data found for user {user_id}")
                return None
            
            # Convert start_date_local to datetime and find the most recent
            existing_data['start_date_local'] = pd.to_datetime(existing_data['start_date_local'])
            most_recent_date = existing_data['start_date_local'].max()
            
            logger.info(f"Most recent activity for user {user_id}: {most_recent_date}")
            return most_recent_date
            
        except Exception as e:
            logger.error(f"Error getting last activity date for user {user_id}: {e}")
            return None
    
    def fetch_new_activities(self, access_token: str, user_id: str, max_pages: int = 20) -> List[Dict[str, Any]]:
        """
        Fetch only new activities since the last stored data.
        
        Args:
            access_token: Strava access token
            user_id: User's Strava ID
            max_pages: Maximum number of pages to fetch
            
        Returns:
            List of new activities
        """
        try:
            # Get the date of the most recent stored activity
            last_activity_date = self.get_last_activity_date(user_id)
            
            if last_activity_date is None:
                logger.info(f"No existing data found for user {user_id}, fetching all activities")
                # If no existing data, fetch all activities
                return self.strava_service.get_activities(access_token, max_pages)
            
            logger.info(f"Fetching activities newer than {last_activity_date} for user {user_id}")
            
            # Fetch activities from Strava API
            url = 'https://www.strava.com/api/v3/athlete/activities'
            headers = {'Authorization': f'Bearer {access_token}'}
            
            new_activities = []
            page = 1
            
            while page <= max_pages:
                try:
                    logger.info(f"Fetching page {page} for incremental update")
                    response = requests.get(url, headers=headers, params={
                        "per_page": 100, 
                        'page': page,
                        'after': int(last_activity_date.timestamp())  # Strava expects Unix timestamp
                    })
                    
                    if response.status_code != 200:
                        logger.error(f"Strava API error: {response.status_code} - {response.text}")
                        break
                    
                    data = response.json()
                    
                    # If no more activities, break
                    if not data:
                        logger.info(f"No more activities found on page {page}")
                        break
                    
                    # Filter activities to only include those newer than our last stored date
                    filtered_activities = []
                    for activity in data:
                        activity_date = datetime.fromisoformat(activity['start_date_local'].replace('Z', '+00:00'))
                        if activity_date > last_activity_date:
                            filtered_activities.append(activity)
                        else:
                            # Since activities are returned in chronological order (newest first),
                            # if we find an older activity, we can stop processing this page
                            logger.info(f"Found activity older than last stored date, stopping at page {page}")
                            break
                    
                    new_activities.extend(filtered_activities)
                    
                    # If we didn't add any activities from this page, we're done
                    if not filtered_activities:
                        logger.info(f"No new activities found on page {page}, stopping")
                        break
                    
                    logger.info(f"Fetched {len(filtered_activities)} new activities from page {page}")
                    page += 1
                    
                except Exception as e:
                    logger.error(f"Error fetching page {page}: {e}")
                    break
            
            logger.info(f"Total new activities fetched: {len(new_activities)}")
            return new_activities
            
        except Exception as e:
            logger.error(f"Error fetching new activities for user {user_id}: {e}")
            # Fallback to fetching all activities if incremental fetch fails
            logger.info("Falling back to full data fetch")
            return self.strava_service.get_activities(access_token, max_pages)
    
    def check_if_incremental_update_needed(self, user_id: str) -> bool:
        """
        Check if an incremental update is possible (i.e., user has existing data).
        
        Args:
            user_id: User's Strava ID
            
        Returns:
            True if incremental update is possible, False if full fetch is needed
        """
        try:
            existing_data = supabase_data_service.get_user_data(user_id)
            return existing_data is not None and not existing_data.empty
        except Exception as e:
            logger.error(f"Error checking if incremental update needed: {e}")
            return False
    
    def get_data_fetch_strategy(self, user_id: str) -> str:
        """
        Determine the best data fetching strategy for a user.
        
        Args:
            user_id: User's Strava ID
            
        Returns:
            'incremental' if incremental fetch is possible, 'full' otherwise
        """
        if self.check_if_incremental_update_needed(user_id):
            return 'incremental'
        else:
            return 'full'