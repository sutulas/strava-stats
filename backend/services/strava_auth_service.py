import requests
import os
from dotenv import load_dotenv
# from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

class StravaAuthService:

    def __init__(self): 
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.redirect_uri = REDIRECT_URI
        self.code = None
        self.access_token = None
        self.refresh_token = None
        
    def get_auth_url(self):
        return f"https://www.strava.com/oauth/authorize?client_id={self.client_id}&response_type=code&redirect_uri={self.redirect_uri}&approval_prompt=force&scope=activity:read_all"

    def get_access_token(self):
        url = "https://www.strava.com/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.code,
            "grant_type": "authorization_code"
        }
        response = requests.post(url, headers=headers, data=data)
        print(response.json())
        return response.json()['access_token']

    def refresh_access_token(self):
        url = "https://www.strava.com/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        } 
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token"
        }
        response = requests.post(url, headers=headers, data=data)
        return response.json()
    
    def get_access(self):
        print(f"Follow the link to authorize the app: \n{self.get_auth_url()}")
        self.code = input("Enter the code:   ")
        token_response = self.get_access_token()
        
        self.access_token = token_response
        return self.access_token
    
        
        
if __name__ == "__main__":
    auth_service = StravaAuthService()
    auth_service.get_access()

