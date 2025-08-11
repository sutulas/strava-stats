import requests
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
import logging

logger = logging.getLogger(__name__)

class StravaDataService:
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.redirect_uri = REDIRECT_URI

    def get_activities(self, token, max_pages=20):
        """Fetch user activities from Strava API"""
        logger.info(f"Fetching activities for token: {token[:10]}...")
        
        url = 'https://www.strava.com/api/v3/athlete/activities'
        headers = {'Authorization': f'Bearer {token}'}
        
        activities = []
        page = 1
        
        while page <= max_pages:
            try:
                logger.info(f"Fetching page {page}")
                response = requests.get(url, headers=headers, params={"per_page": 100, 'page': page})
                
                if response.status_code != 200:
                    logger.error(f"Strava API error: {response.status_code} - {response.text}")
                    break
                
                data = response.json()
                
                # If no more activities, break
                if not data:
                    logger.info(f"No more activities found on page {page}")
                    break
                
                activities.extend(data)
                logger.info(f"Fetched {len(data)} activities from page {page}")
                
                page += 1
                
            except Exception as e:
                logger.error(f"Error fetching page {page}: {e}")
                break
        
        logger.info(f"Total activities fetched: {len(activities)}")
        return activities
    
    def get_user_profile(self, token):
        """Fetch user profile from Strava API"""
        try:
            url = 'https://www.strava.com/api/v3/athlete'
            headers = {'Authorization': f'Bearer {token}'}
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to fetch user profile: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching user profile: {e}")
            return None
    