import time
from video_creator import create_video  # Import the create_video function

def main():
    # Set the total video duration (e.g., 60 seconds per video)
    total_video_duration = 60
    
    # Initialize the video creation generator
    video_generator = create_video(total_video_duration)
    
    # Iterate over the generator to create videos indefinitely
    for created_videos in video_generator:
        print(f"Videos created: {created_videos}")
        # Optional: Add further logic to process the videos
        time.sleep(5)  # Optional sleep time before creating the next batch of videos

if __name__ == "__main__":
    main()
