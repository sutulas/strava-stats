"""
Rate limiting service for Strava Stats API.

This service provides in-memory rate limiting functionality that limits users
to 3 queries per session. It uses a simple 
dictionary to track query counts per access token, which resets when the user 
logs out and logs back in.
"""

from typing import Dict, Optional
from datetime import datetime
import logging
import requests

logger = logging.getLogger(__name__)

class RateLimitingService:
    """
    In-memory rate limiting service that tracks query counts per access token.
    
    This service maintains a simple dictionary mapping access tokens to their
    query counts. When a user logs out and logs back in, they get a new access
    token, effectively resetting their rate limit.
    """
    
    def __init__(self, max_queries: int = 3):
        """
        Initialize the rate limiting service.
        
        Args:
            max_queries: Maximum number of queries allowed per session (default: 3)
        """
        self.max_queries = max_queries
        self.query_counts: Dict[str, int] = {}
        self.session_start_times: Dict[str, datetime] = {}
        self.user_max_queries: Dict[str, int] = {}  # Track max queries per user
        
    def _get_user_profile_name(self, access_token: str) -> Optional[str]:
        """
        Get the user's full name from Strava API.
        
        Args:
            access_token: The user's Strava access token
            
        Returns:
            Full name (firstname lastname) or None if unable to fetch
        """
        try:
            url = 'https://www.strava.com/api/v3/athlete'
            headers = {'Authorization': f'Bearer {access_token}'}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                profile_data = response.json()
                firstname = profile_data.get('firstname', '')
                lastname = profile_data.get('lastname', '')
                full_name = f"{firstname} {lastname}".strip()
                logger.info(f"Retrieved profile name: {full_name}")
                return full_name
            else:
                logger.warning(f"Failed to fetch user profile: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching user profile: {e}")
            return None
    
    def _get_user_max_queries(self, access_token: str) -> int:
        """
        Determine the maximum queries allowed for a user based on their profile.
        
        Args:
            access_token: The user's Strava access token
            
        Returns:
            Maximum number of queries allowed for this user
        """
        # Check if we already have this user's max queries cached
        if access_token in self.user_max_queries:
            return self.user_max_queries[access_token]
        
        # Get user profile name
        profile_name = self._get_user_profile_name(access_token)
        
        # Determine max queries based on profile name
        if profile_name == "Seamus Sutula":
            max_queries = 30
            logger.info(f"Special user detected: {profile_name} - granting 30 queries")
        else:
            max_queries = self.max_queries
            logger.info(f"Standard user: {profile_name or 'Unknown'} - granting {max_queries} queries")
        
        # Cache the result
        self.user_max_queries[access_token] = max_queries
        return max_queries
        
    def can_make_query(self, access_token: str) -> bool:
        """
        Check if a user can make a query based on their current usage.
        
        Args:
            access_token: The user's Strava access token
            
        Returns:
            True if the user can make a query, False otherwise
        """
        if not access_token:
            return False
            
        current_count = self.query_counts.get(access_token, 0)
        user_max_queries = self._get_user_max_queries(access_token)
        return current_count < user_max_queries
    
    def record_query(self, access_token: str) -> bool:
        """
        Record a query attempt and return whether it was allowed.
        
        Args:
            access_token: The user's Strava access token
            
        Returns:
            True if the query was allowed, False if rate limited
        """
        if not access_token:
            return False
            
        # Check if this is a new session
        if access_token not in self.query_counts:
            self.query_counts[access_token] = 0
            self.session_start_times[access_token] = datetime.now()
            logger.info(f"New session started for token: {access_token[:10]}...")
        
        # Check rate limit
        if not self.can_make_query(access_token):
            logger.warning(f"Rate limit exceeded for token: {access_token[:10]}...")
            return False
        
        # Increment query count
        self.query_counts[access_token] += 1
        current_count = self.query_counts[access_token]
        user_max_queries = self._get_user_max_queries(access_token)
        
        logger.info(f"Query recorded for token: {access_token[:10]}... (count: {current_count}/{user_max_queries})")
        return True
    
    def get_remaining_queries(self, access_token: str) -> int:
        """
        Get the number of remaining queries for a user.
        
        Args:
            access_token: The user's Strava access token
            
        Returns:
            Number of remaining queries (0 if rate limited)
        """
        if not access_token:
            return 0
            
        current_count = self.query_counts.get(access_token, 0)
        user_max_queries = self._get_user_max_queries(access_token)
        return max(0, user_max_queries - current_count)
    
    def get_query_count(self, access_token: str) -> int:
        """
        Get the current query count for a user.
        
        Args:
            access_token: The user's Strava access token
            
        Returns:
            Current query count for the user
        """
        if not access_token:
            return 0
            
        return self.query_counts.get(access_token, 0)
    
    def reset_user_queries(self, access_token: str) -> None:
        """
        Reset the query count for a specific user (useful for testing or admin functions).
        
        Args:
            access_token: The user's Strava access token
        """
        if access_token in self.query_counts:
            del self.query_counts[access_token]
        if access_token in self.session_start_times:
            del self.session_start_times[access_token]
        if access_token in self.user_max_queries:
            del self.user_max_queries[access_token]
        logger.info(f"Query count reset for token: {access_token[:10]}...")
    
    def get_session_info(self, access_token: str) -> Dict[str, any]:
        """
        Get session information for a user.
        
        Args:
            access_token: The user's Strava access token
            
        Returns:
            Dictionary containing session information
        """
        if not access_token:
            return {
                "query_count": 0,
                "remaining_queries": 0,
                "max_queries": self.max_queries,
                "session_start": None,
                "rate_limited": True
            }
        
        current_count = self.query_counts.get(access_token, 0)
        session_start = self.session_start_times.get(access_token)
        user_max_queries = self._get_user_max_queries(access_token)
        
        return {
            "query_count": current_count,
            "remaining_queries": self.get_remaining_queries(access_token),
            "max_queries": user_max_queries,
            "session_start": session_start.isoformat() if session_start else None,
            "rate_limited": current_count >= user_max_queries
        }
    
    def cleanup_old_sessions(self, max_age_hours: int = 24) -> int:
        """
        Clean up old sessions to prevent memory leaks.
        
        Args:
            max_age_hours: Maximum age of sessions in hours before cleanup
            
        Returns:
            Number of sessions cleaned up
        """
        from datetime import timedelta
        
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        sessions_to_remove = []
        
        for token, start_time in self.session_start_times.items():
            if start_time < cutoff_time:
                sessions_to_remove.append(token)
        
        for token in sessions_to_remove:
            self.reset_user_queries(token)
        
        if sessions_to_remove:
            logger.info(f"Cleaned up {len(sessions_to_remove)} old sessions")
        
        return len(sessions_to_remove)

# Global instance
rate_limiter = RateLimitingService()