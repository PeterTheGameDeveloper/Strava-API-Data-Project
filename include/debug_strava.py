import os
import sys
import datetime
from strava_client import StravaClient

# Ensure we can import from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_strava():
    print("Starting Strava Debug Script...")
    
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')
    
    print(f"Client ID present: {bool(client_id)}")
    print(f"Client Secret present: {bool(client_secret)}")
    print(f"Refresh Token present: {bool(refresh_token)}")
    
    if not all([client_id, client_secret, refresh_token]):
        print("ERROR: Missing environment variables.")
        return

    try:
        client = StravaClient(client_id, client_secret, refresh_token)
        print("Client initialized.")
        
        # Try a simple fetch
        # Calculate timestamp for 1 day ago
        days_back = 1
        after_timestamp = int((datetime.datetime.now() - datetime.timedelta(days=days_back)).timestamp())
        
        print(f"Fetching activities since timestamp: {after_timestamp}")
        activities = client.get_activities(after_timestamp=after_timestamp, per_page=1)
        print(f"Success! Fetched {len(activities)} activities.")
        if activities:
            print("Sample activity ID:", activities[0].get('id'))
            
    except Exception as e:
        print(f"\nCRITICAL FAILURE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_strava()
