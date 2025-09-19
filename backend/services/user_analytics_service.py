import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Any, Optional
import pytz
import os

logger = logging.getLogger(__name__)

class UserAnalyticsService:
    def __init__(self):
        pass
    
    def get_user_profile_data(self, access_token: str) -> Dict[str, Any]:
        """Get user profile information from Strava"""
        try:
            import requests
            
            url = 'https://www.strava.com/api/v3/athlete'
            headers = {'Authorization': f'Bearer {access_token}'}
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                profile_data = response.json()
                return {
                    'id': profile_data.get('id'),
                    'firstname': profile_data.get('firstname'),
                    'lastname': profile_data.get('lastname'),
                    'username': profile_data.get('username'),
                    'city': profile_data.get('city'),
                    'state': profile_data.get('state'),
                    'country': profile_data.get('country'),
                    'weight': profile_data.get('weight'),
                    'profile': profile_data.get('profile'),
                    'profile_medium': profile_data.get('profile_medium'),
                    'follower_count': profile_data.get('follower_count'),
                    'friend_count': profile_data.get('friend_count'),
                    'date_preference': profile_data.get('date_preference'),
                    'measurement_preference': profile_data.get('measurement_preference')
                }
            else:
                logger.error(f"Failed to fetch user profile: {response.status_code}")
                # Return error information instead of empty dict
                error_detail = response.json().get('message', 'Unknown error') if response.content else 'No response content'
                raise Exception(f"Strava API error {response.status_code}: {error_detail}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching user profile: {e}")
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            logger.error(f"Error fetching user profile: {e}")
            raise Exception(f"Failed to fetch user profile: {str(e)}")
    
    def get_user_stats(self, df: pd.DataFrame = None) -> Dict[str, Any]:
        """Calculate comprehensive user statistics from processed data"""
        try:
            if df is None:
                return {"error": "No data provided"}
            
            if df.empty:
                return {"error": "No data available"}
            
            # Basic stats
            total_runs = len(df)
            total_miles = df['distance'].sum()
            total_time_minutes = df['moving_time'].sum()
            total_elevation = df['total_elevation_gain'].sum()
            
            # Average stats
            avg_pace = df['average_speed'].mean()
            avg_distance = df['distance'].mean()
            avg_time = df['moving_time'].mean()
            avg_heartrate = df['average_heartrate'].mean() if 'average_heartrate' in df.columns else None
            
            # Best stats
            fastest_pace = df['average_speed'].min()
            longest_run = df['distance'].max()
            longest_time = df['moving_time'].max()
            
            # Time-based stats - Fix timezone issues
            df['start_date_local'] = pd.to_datetime(df['start_date_local'])
            
            # Convert to timezone-naive datetime for comparison
            df['start_date_local'] = df['start_date_local'].dt.tz_localize(None)
            
            current_year = datetime.now().year
            this_year_runs = df[df['start_date_local'].dt.year == current_year]
            this_year_miles = this_year_runs['distance'].sum()
            
            # Weekly stats for the past 8 weeks
            eight_weeks_ago = datetime.now() - timedelta(weeks=8)
            # Remove timezone info for comparison
            eight_weeks_ago = eight_weeks_ago.replace(tzinfo=None)
            
            recent_data = df[df['start_date_local'] >= eight_weeks_ago].copy()
            
            weekly_stats = []
            if not recent_data.empty:
                recent_data['week_start'] = recent_data['start_date_local'].dt.to_period('W-MON').dt.start_time
                weekly_groups = recent_data.groupby('week_start')
                
                for week_start, week_data in weekly_groups:
                    weekly_stats.append({
                        'week_start': week_start.strftime('%Y-%m-%d'),
                        'runs': len(week_data),
                        'miles': week_data['distance'].sum(),
                        'avg_pace': week_data['average_speed'].mean(),
                        'total_time': week_data['moving_time'].sum()
                    })
            
            # Monthly stats for the past 12 months
            twelve_months_ago = datetime.now() - timedelta(days=365)
            # Remove timezone info for comparison
            twelve_months_ago = twelve_months_ago.replace(tzinfo=None)
            
            monthly_data = df[df['start_date_local'] >= twelve_months_ago].copy()
            
            monthly_stats = []
            if not monthly_data.empty:
                monthly_data['month'] = monthly_data['start_date_local'].dt.to_period('M')
                monthly_groups = monthly_data.groupby('month')
                
                for month, month_data in monthly_groups:
                    monthly_stats.append({
                        'month': month.strftime('%Y-%m'),
                        'runs': len(month_data),
                        'miles': month_data['distance'].sum(),
                        'avg_pace': month_data['average_speed'].mean(),
                        'total_time': month_data['moving_time'].sum()
                    })
            
            # Day of week analysis
            day_of_week_stats = df.groupby('day_of_week').agg({
                'distance': ['count', 'sum', 'mean'],
                'average_speed': 'mean',
                'moving_time': 'sum'
            }).round(2)
            
            # Convert to more readable format
            day_stats = []
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
                if day in day_of_week_stats.index:
                    day_data = day_of_week_stats.loc[day]
                    day_stats.append({
                        'day': day,
                        'runs': int(day_data[('distance', 'count')]),
                        'miles': round(day_data[('distance', 'sum')], 2),
                        'avg_distance': round(day_data[('distance', 'mean')], 2),
                        'avg_pace': round(day_data[('average_speed', 'mean')], 2),
                        'total_time': round(day_data[('moving_time', 'sum')], 2)
                    })
                else:
                    day_stats.append({
                        'day': day,
                        'runs': 0,
                        'miles': 0,
                        'avg_distance': 0,
                        'avg_pace': 0,
                        'total_time': 0
                    })
            
            return {
                'summary': {
                    'total_runs': int(total_runs),
                    'total_miles': round(total_miles, 2),
                    'total_time_minutes': round(total_time_minutes, 2),
                    'total_elevation': round(total_elevation, 2),
                    'this_year_miles': round(this_year_miles, 2)
                },
                'averages': {
                    'avg_pace': round(avg_pace, 2) if not pd.isna(avg_pace) else None,
                    'avg_distance': round(avg_distance, 2),
                    'avg_time': round(avg_time, 2),
                    'avg_heartrate': round(avg_heartrate, 1) if avg_heartrate and not pd.isna(avg_heartrate) else None
                },
                'bests': {
                    'fastest_pace': round(fastest_pace, 2) if not pd.isna(fastest_pace) else None,
                    'longest_run': round(longest_run, 2),
                    'longest_time': round(longest_time, 2)
                },
                'weekly_stats': weekly_stats,
                'monthly_stats': monthly_stats,
                'day_of_week_stats': day_stats
            }
            
        except Exception as e:
            logger.error(f"Error calculating user stats: {e}")
            return {"error": f"Failed to calculate stats: {str(e)}"}
    
    def get_recent_activities(self, df: pd.DataFrame = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent running activities"""
        try:
            if df is None:
                return []
            
            if df.empty:
                return []
            
            # Sort by date and get recent activities
            df['start_date_local'] = pd.to_datetime(df['start_date_local'])
            # Convert to timezone-naive datetime
            df['start_date_local'] = df['start_date_local'].dt.tz_localize(None)
            df = df.sort_values('start_date_local', ascending=False)
            
            recent_activities = df.head(limit).to_dict('records')
            
            # Format the data for frontend
            formatted_activities = []
            for activity in recent_activities:
                formatted_activities.append({
                    'id': activity['id'],
                    'name': activity['name'],
                    'date': activity['start_date_local'],
                    'distance': round(activity['distance'], 2),
                    'time': round(activity['moving_time'], 2),
                    'pace': round(activity['average_speed'], 2) if not pd.isna(activity['average_speed']) else None,
                    'elevation': round(activity['total_elevation_gain'], 2),
                    'heartrate': round(activity['average_heartrate'], 1) if 'average_heartrate' in activity and not pd.isna(activity['average_heartrate']) else None
                })
            
            return formatted_activities
            
        except Exception as e:
            logger.error(f"Error getting recent activities: {e}")
            return [] 