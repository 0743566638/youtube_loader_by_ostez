# Filename: automate/auto.py

import os
import http.client
import httplib2
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from automate.videoText import get_random_title_and_description, get_random_hashtags
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import random
import re

# Fix the CLIENT_SECRETS_FILE path to use relative path
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "client.json")

# Get the base directory of the project to build correct paths
# This ensures that all file paths are relative to the project root, not the current script directory.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The SCOPES list contains the permissions your app needs.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# The path to the folder containing the video to upload.
VIDEO_FOLDER_PATH = os.path.join(BASE_DIR, "finalvideos")

def get_authenticated_service(credentials_file_path):
    """
    Authenticates the user using a specific credentials file and returns the YouTube API service object.
    
    This function first checks for existing valid credentials before requesting new ones.
    """
    credentials = None
    
    # Check if credentials file exists
    if os.path.exists(credentials_file_path):
        try:
            credentials = Credentials.from_authorized_user_file(credentials_file_path, SCOPES)
            print(f"✅ Loaded existing credentials from: {credentials_file_path}")
        except Exception as e:
            print(f"⚠️  Could not load existing credentials: {e}")
            credentials = None
    
    # If no valid credentials available, let the user log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                print("�� Refreshing expired credentials...")
                credentials.refresh(Request())
                print("✅ Credentials refreshed successfully!")
            except Exception as e:
                print(f"❌ Failed to refresh credentials: {e}")
                credentials = None
        
        if not credentials:
            print("🔐 No valid credentials found. Starting OAuth2 flow...")
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
                credentials = flow.run_local_server(port=0)
                print("✅ New credentials obtained successfully!")
            except Exception as e:
                print(f"❌ OAuth2 flow failed: {e}")
                raise
        
        # Save the credentials for the next run
        try:
            with open(credentials_file_path, 'w') as token:
                token.write(credentials.to_json())
            print(f"💾 Credentials saved to: {credentials_file_path}")
        except Exception as e:
            print(f"⚠️  Warning: Could not save credentials: {e}")
    
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def upload_video(youtube, video_file_path, title, description):
    """Uploads a video and its metadata to YouTube."""
    # Get random hashtags for tags
    tags = get_random_hashtags(30)
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    media_body = MediaFileUpload(video_file_path, chunksize=-1, resumable=True)

    try:
        print(f"Uploading file: {video_file_path}")
        insert_request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media_body
        )
        
        response = resumable_upload(insert_request)
        print("Video upload successful!")
        return response
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def resumable_upload(request):
    """Handles the resumable upload process."""
    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"Upload progress: {int(status.progress() * 100)}%")
        except httplib2.HttpLib2Error as e:
            print(f"An HTTP error occurred during upload: {e}")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    return response

def delete_video(video_file_name):
    """Deletes the video file from the finalvideos folder."""
    video_path = os.path.join(VIDEO_FOLDER_PATH, video_file_name)
    if os.path.exists(video_path):
        try:
            os.remove(video_path)
            print(f"Deleted video file: {video_file_name}")
        except Exception as e:
            print(f"Failed to delete video file: {e}")
    else:
        print(f"Video file {video_file_name} not found.")

def get_latest_video_file():
    """Get the most recent video file from the finalvideos folder."""
    try:
        video_files = [f for f in os.listdir(VIDEO_FOLDER_PATH) if f.endswith('.mp4')]
        if not video_files:
            return None
        
        # Get the most recent file by modification time
        latest_file = max(video_files, key=lambda f: os.path.getmtime(os.path.join(VIDEO_FOLDER_PATH, f)))
        return latest_file
    except Exception as e:
        print(f"Error finding latest video file: {e}")
        return None

def automate_process(channel_name):
    """Function to run the automated upload for a specific channel."""
    # Find the most recent video file instead of hardcoded name
    video_file_name = get_latest_video_file()
    if not video_file_name:
        print("Error: No video files found in the finalvideos folder")
        return False
    
    video_file_path = os.path.join(VIDEO_FOLDER_PATH, video_file_name)
    print(f"Found video file: {video_file_name}")

    title, description = get_random_title_and_description()

    # Create credentials directory if it doesn't exist
    credentials_dir = os.path.join(BASE_DIR, "credentials")
    os.makedirs(credentials_dir, exist_ok=True)
    credentials_file_path = os.path.join(credentials_dir, f"{channel_name}_credentials.json")

    try:
        youtube = get_authenticated_service(credentials_file_path)
    except Exception as e:
        print(f"Authentication failed: {e}")
        return False

    if os.path.exists(video_file_path):
        uploaded_video = upload_video(youtube, video_file_path, title, description)
        if uploaded_video:
            print(f"Video uploaded with ID: {uploaded_video['id']}")
            delete_video(video_file_name)
            return True
        else:
            print("Video upload failed.")
            return False
    else:
        print(f"Error: Video file not found at {video_file_path}")
        return False

if __name__ == '__main__':
    # Use the correct channel name
    channel = "SleepRelaxAndMeditates"
    print(f"Attempting to automate video upload for channel: {channel}")
    automate_process(channel)