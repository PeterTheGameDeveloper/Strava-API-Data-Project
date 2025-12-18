import requests
import time
import os

class StravaClient:
    def __init__(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.auth_url = "https://www.strava.com/oauth/token"
        self.base_url = "https://www.strava.com/api/v3"
        self.access_token = None

    def refresh_access_token(self):
        """
        Exchanges the refresh token for a new access token.
        """
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token',
        }
        
        try:
            response = requests.post(self.auth_url, data=payload)
            response.raise_for_status()
            data = response.json()
            self.access_token = data['access_token']
            new_refresh_token = data.get('refresh_token')
            
            if new_refresh_token and new_refresh_token != self.refresh_token:
                print(f"ALERT: Refresh token has been rotated! Please update your STRAVA_REFRESH_TOKEN environment variable to: {new_refresh_token}")
                self.refresh_token = new_refresh_token
                
            print("Successfully refreshed access token.")
        except requests.exceptions.HTTPError as e:
            print(f"Error refreshing access token: {e}")
            print(f"Response body: {response.text}")
            raise e

    def get_activities(self, after_timestamp=None, per_page=200):
        """
        Fetches activities after a specific timestamp.
        """
        if not self.access_token:
            self.refresh_access_token()
            
        activities = []
        page = 1
        
        while True:
            params = {'per_page': per_page, 'page': page}
            if after_timestamp:
                params['after'] = after_timestamp
            
            headers = {'Authorization': f'Bearer {self.access_token}'}
            response = requests.get(f"{self.base_url}/athlete/activities", headers=headers, params=params)
            
            if response.status_code == 429:
                print("Rate limited. Waiting 15 minutes...")
                time.sleep(900)
                continue

            if response.status_code == 401:
                print("Received 401 Unauthorized. Attempting to refresh access token and retry...")
                try:
                    self.refresh_access_token()
                    headers = {'Authorization': f'Bearer {self.access_token}'}
                    response = requests.get(f"{self.base_url}/athlete/activities", headers=headers, params=params)
                except Exception as e:
                    print(f"Failed to recover from 401: {e}")
                    raise
            
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(f"HTTP Error in get_activities: {e}")
                print(f"Response body: {response.text}")
                raise e

            data = response.json()
            
            if not data:
                break
                
            activities.extend(data)
            print(f"Fetched page {page} with {len(data)} activities.")
            page += 1
            
        return activities
