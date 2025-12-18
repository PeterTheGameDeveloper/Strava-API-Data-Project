import requests
import os
import sys

# Try to load env vars from .env file if not present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def get_strava_tokens():
    print("--- Strava Re-Authorization Helper ---")
    
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    
    # Allow user to input if not in env
    if not client_id:
        client_id = input("Enter your Strava Client ID: ").strip()
    if not client_secret:
        client_secret = input("Enter your Strava Client Secret: ").strip()
        
    if not client_id or not client_secret:
        print("Error: Client ID and Secret are required.")
        return

    # 1. Generate Auth URL
    redirect_uri = "http://localhost/exchange_token"
    scope = "activity:read_all"
    auth_url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={client_id}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&approval_prompt=force"
        f"&scope={scope}"
    )
    
    print(f"\n1. Please visit the following URL in your browser:\n")
    print(f"{auth_url}\n")
    print("2. Click 'Authorize'.")
    print("3. You will be redirected to a page (that might fail to load, that's okay).")
    print("4. Copy the 'code' parameter from the URL address bar.")
    print("   (e.g. http://localhost/exchange_token?state=&code=YOUR_CODE_HERE&scope=...)")
    
    code = input("\nEnter the code here: ").strip()
    
    if not code:
        print("No code entered.")
        return

    # 2. Exchange code for tokens
    print("\nExchanging code for tokens...")
    token_url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    
    response = requests.post(token_url, data=payload)
    
    if response.status_code != 200:
        print(f"Error exchanging token: {response.text}")
        return
        
    data = response.json()
    
    refresh_token = data.get('refresh_token')
    access_token = data.get('access_token')
    
    print("\n--- SUCCESS! ---")
    print(f"New Refresh Token: {refresh_token}")
    print(f"New Access Token:  {access_token}")
    print("\nPlease update your .env file and docker-compose.yaml with this new STRAVA_REFRESH_TOKEN.")

if __name__ == "__main__":
    get_strava_tokens()
