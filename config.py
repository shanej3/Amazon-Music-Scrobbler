import os 
import asyncio
import time
from dotenv import load_dotenv
import pylast

load_dotenv()

API_KEY = os.getenv("LASTFM_API_KEY")
API_SECRET = os.getenv("LASTFM_API_SECRET")
SESSION_KEY = os.getenv("LASTFM_SESSION_KEY")

async def get_network():
    # Reload .env each time to pick up updated SESSION_KEY
    load_dotenv(override=True)
    current_session_key = os.getenv("LASTFM_SESSION_KEY")
    
    # Use existing session key if available, otherwise get a new one
    session_key = current_session_key if current_session_key else await get_new_session_key(API_KEY, API_SECRET)
    
    network = pylast.LastFMNetwork(
        api_key=API_KEY,
        api_secret=API_SECRET,
        session_key=session_key
    )
    return network

import webbrowser
import pylast

async def get_new_session_key(api_key: str, api_secret: str) -> str:
    network = pylast.LastFMNetwork(
        api_key=api_key,
        api_secret=api_secret
    )

    # Generate authorization URL
    sg = pylast.SessionKeyGenerator(network)
    auth_url = sg.get_web_auth_url()

    print("Opening browser for Last.fm authorization...")
    webbrowser.open(auth_url)
    
    print("\nAuthorizing in browser... waiting 15 seconds to complete authorization.")
    for i in range(15, 0, -1):
        print(f"Time remaining: {i}s", end='\r')
        time.sleep(1)

    # Exchange authorization for session key
    try:
        session_key = sg.get_web_auth_session_key(auth_url)
        print(f"Successfully obtained session key: {session_key}")
        
        # Read .env file and check if LASTFM_SESSION_KEY already exists
        env_path = ".env"
        env_content = ""
        key_found = False
        
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                env_content = f.read()
            key_found = "LASTFM_SESSION_KEY=" in env_content
        
        if key_found:
            # Replace existing key
            env_content = "\n".join(
                f"LASTFM_SESSION_KEY={session_key}" if line.startswith("LASTFM_SESSION_KEY=") else line
                for line in env_content.split("\n")
            )
        else:
            # Append new key
            env_content += f"\nLASTFM_SESSION_KEY={session_key}"
        
        with open(env_path, "w") as f:
            f.write(env_content)
    
        
        # Reload the environment so SESSION_KEY gets updated
        load_dotenv(override=True)
        verify_key = os.getenv("LASTFM_SESSION_KEY")
        print("Session key saved to .env")
        
        return session_key
    except pylast.WSError as e:
        print(f"Failed to fetch session key: {e}")
        return None