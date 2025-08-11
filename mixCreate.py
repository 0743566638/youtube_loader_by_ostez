import os
import random
import datetime
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import ffmpeg

# Define supported file extensions
AUDIO_EXTENSIONS = ('.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg')
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

# Cross-platform folder paths using os.path.join
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC_FOLDER = os.path.join(BASE_DIR, "music")
IMAGES_FOLDER = os.path.join(BASE_DIR, "images")
FINAL_VIDEOS_FOLDER = os.path.join(BASE_DIR, "finalvideos")
TEMP_FILES_FOLDER = os.path.join(BASE_DIR, "tempFiles")
OVERLAY_VIDEO_PATH = os.path.join(BASE_DIR, "myAssets", "subscribe.mp4")

# Optimized settings for speed and quality
AUDIO_CHUNK_DURATION = 60  # in seconds
IMAGE_DURATION = 10  # in seconds
OUTPUT_RESOLUTION = (1280, 720)  # Output resolution optimized for speed
VIDEO_FPS = 24  # Lower FPS for faster processing
AUDIO_BITRATE = '256k'
VIDEO_PRESET = 'ultrafast'

# Performance optimization flags
CLEANUP_TEMP_FILES = True

class VideoProgressTracker:
    """Thread-safe progress tracker for video processing"""
    def __init__(self):
        self.progress = 0
        self.status = "Initializing..."
        self.lock = threading.Lock()
    
    def update(self, progress, status):
        with self.lock:
            self.progress = progress
            self.status = status
    
    def get_status(self):
        with self.lock:
            return self.progress, self.status

def ensure_directory_exists(directory_path):
    """Ensure directory exists, create if it doesn't"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")

def get_supported_files(folder_path, extensions):
    """Get list of supported files with proper error handling"""
    try:
        if not os.path.exists(folder_path):
            print(f"Warning: Directory {folder_path} does not exist")
            return []
        
        files = [os.path.join(folder_path, file) for file in os.listdir(folder_path)
                 if any(file.lower().endswith(ext) for ext in extensions)]
        
        if not files:
            print(f"Warning: No supported files found in {folder_path}")
        
        return files
    except Exception as e:
        print(f"Error scanning directory {folder_path}: {e}")
        return []

def cleanup_temp_files(file_paths):
    """Clean up temporary files with proper error handling"""
    for file_path in file_paths:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Cleaned up temporary file: {file_path}")
            except PermissionError:
                print(f"Warning: Could not delete {file_path} - file may still be in use")
            except Exception as e:
                print(f"Warning: Error cleaning up {file_path}: {e}")

def create_audio_mix_ffmpeg(audio_files, total_video_duration, temp_file_path):
    """Generates an optimized audio mix using FFmpeg's concat protocol."""
    if not audio_files:
        raise ValueError("No audio files provided")

    audio_list = []
    total_duration = 0
    available_files = audio_files[:]

    # Prepare audio list for the desired duration
    while total_duration < total_video_duration and available_files:
        audio_file = random.choice(available_files)
        # We need a robust way to get duration without loading the file fully
        # A simple ffprobe call is more efficient
        try:
            probe = ffmpeg.probe(audio_file)
            duration = float(probe['format']['duration'])
        except Exception as e:
            print(f"Warning: Failed to probe duration for {audio_file}. Skipping. Error: {e}")
            available_files.remove(audio_file)
            continue
        
        audio_list.append(audio_file)
        total_duration += duration

    if not audio_list:
        raise ValueError("No valid audio files could be processed for mixing.")

    # Create a text file with the list of audio files to concatenate
    concat_list_path = os.path.join(os.path.dirname(temp_file_path), "concat_audio_list.txt")
    with open(concat_list_path, 'w') as f:
        for file in audio_list:
            f.write(f"file '{file}'\n")

    # Use ffmpeg-python to concatenate the audio files
    print("Concatenating audio files with FFmpeg...")
    try:
        print(f"🔧 Audio FFmpeg command details:")
        print(f"   Input list: {concat_list_path}")
        print(f"   Output: {temp_file_path}")
        print(f"   Bitrate: {AUDIO_BITRATE}")
        
        (
            ffmpeg
            .input(concat_list_path, format='concat', safe=0)
            .output(temp_file_path, acodec='aac', ar=44100, ab=AUDIO_BITRATE)
            .overwrite_output()
            .run(cmd=['ffmpeg', '-y'], capture_stderr=True, quiet=True)
        )
        
        # Verify the output file was created
        if not os.path.exists(temp_file_path):
            raise FileNotFoundError(f"FFmpeg audio completed but output file not found: {temp_file_path}")
        
        file_size = os.path.getsize(temp_file_path)
        if file_size == 0:
            raise ValueError(f"FFmpeg audio completed but output file is empty: {temp_file_path}")
        
        print(f"✅ Temporary audio created successfully: {temp_file_path} ({file_size} bytes)")
        
    except ffmpeg.Error as e:
        print(f"❌ FFmpeg audio concatenation failed:")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"   Error details: {e.stderr.decode('utf8')}")
        else:
            print(f"   Error: {e}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error during audio generation: {e}")
        raise

    os.remove(concat_list_path)
    return temp_file_path

def create_image_slideshow_ffmpeg(image_files, total_video_duration, temp_file_path):
    """Generates an image slideshow video using FFmpeg from a list of images."""
    if not image_files:
        raise ValueError("No image files provided")

    image_list_path = os.path.join(os.path.dirname(temp_file_path), "image_list.txt")
    with open(image_list_path, 'w') as f:
        # Create a list of images with their durations
        for img in image_files:
            f.write(f"file '{img}'\n")
            f.write(f"duration {IMAGE_DURATION}\n")
        # Ensure the last image duration is explicitly set
        f.write(f"file '{image_files[-1]}'\n")

    print("Creating image slideshow with FFmpeg...")
    try:
        print(f"🔧 FFmpeg command details:")
        print(f"   Input: {image_list_path}")
        print(f"   Output: {temp_file_path}")
        print(f"   Resolution: {OUTPUT_RESOLUTION[0]}x{OUTPUT_RESOLUTION[1]}")
        print(f"   Duration: {total_video_duration}s")
        
        (
            ffmpeg
            .input(image_list_path, format='concat', safe=0, t=total_video_duration)
            .filter('scale', size=f"{OUTPUT_RESOLUTION[0]}x{OUTPUT_RESOLUTION[1]}", force_original_aspect_ratio='decrease')
            .filter('pad', w=OUTPUT_RESOLUTION[0], h=OUTPUT_RESOLUTION[1], x='(ow-iw)/2', y='(oh-ih)/2')
            .output(temp_file_path, vcodec='libx264', pix_fmt='yuv420p', preset=VIDEO_PRESET, r=VIDEO_FPS)
            .overwrite_output()
            .run(cmd=['ffmpeg', '-y'], capture_stderr=True, quiet=True)
        )
        
        # Verify the output file was created
        if not os.path.exists(temp_file_path):
            raise FileNotFoundError(f"FFmpeg completed but output file not found: {temp_file_path}")
        
        file_size = os.path.getsize(temp_file_path)
        if file_size == 0:
            raise ValueError(f"FFmpeg completed but output file is empty: {temp_file_path}")
        
        print(f"✅ Temporary video created successfully: {temp_file_path} ({file_size} bytes)")
        
    except ffmpeg.Error as e:
        print(f"❌ FFmpeg video generation failed:")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"   Error details: {e.stderr.decode('utf8')}")
        else:
            print(f"   Error: {e}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error during video generation: {e}")
        raise

    os.remove(image_list_path)
    return temp_file_path

def generate_video_ffmpeg(audio_files, image_files, final_videos_folder, total_video_duration, progress_tracker=None):
    """Main function to generate video using ffmpeg-python for optimized performance."""
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    final_video_path = os.path.join(final_videos_folder, f"video_{timestamp}.mp4")
    
    temp_audio_path = os.path.join(TEMP_FILES_FOLDER, f"temp_audio_{timestamp}.aac")
    temp_video_path = os.path.join(TEMP_FILES_FOLDER, f"temp_video_{timestamp}.mp4")
    
    temp_files_to_clean = [temp_audio_path, temp_video_path]
    
    try:
        if progress_tracker:
            progress_tracker.update(10, "Creating temporary audio mix with FFmpeg...")
        temp_audio_path = create_audio_mix_ffmpeg(audio_files, total_video_duration, temp_audio_path)
        
        if progress_tracker:
            progress_tracker.update(30, "Creating temporary image slideshow with FFmpeg...")
        temp_video_path = create_image_slideshow_ffmpeg(image_files, total_video_duration, temp_video_path)
        
        if progress_tracker:
            progress_tracker.update(70, "Merging audio and video streams with FFmpeg...")
        
        # Use FFmpeg to merge the temporary video and audio files
        print(f"🔧 Final merge FFmpeg command details:")
        print(f"   Video input: {temp_video_path}")
        print(f"   Audio input: {temp_audio_path}")
        print(f"   Output: {final_video_path}")
        
        # Verify temporary files exist before merging
        if not os.path.exists(temp_video_path):
            raise FileNotFoundError(f"Temporary video file not found: {temp_video_path}")
        if not os.path.exists(temp_audio_path):
            raise FileNotFoundError(f"Temporary audio file not found: {temp_audio_path}")
        
        audio_stream = ffmpeg.input(temp_audio_path)
        video_stream = ffmpeg.input(temp_video_path)
        
        (
            ffmpeg
            .output(video_stream, audio_stream, final_video_path, vcodec='copy', acodec='copy')
            .overwrite_output()
            .run(cmd=['ffmpeg', '-y'], capture_stderr=True, quiet=True)
        )
        
        # Verify the final output file was created
        if not os.path.exists(final_video_path):
            raise FileNotFoundError(f"FFmpeg merge completed but final video not found: {final_video_path}")
        
        final_file_size = os.path.getsize(final_video_path)
        if final_file_size == 0:
            raise ValueError(f"FFmpeg merge completed but final video is empty: {final_video_path}")
        
        print(f"✅ Final video merge completed: {final_video_path} ({final_file_size} bytes)")
        
        if progress_tracker:
            progress_tracker.update(100, "Video creation completed!")
        
        print(f"✅ Final video created successfully at: {final_video_path}")
        
        if os.path.exists(final_video_path) and os.path.getsize(final_video_path) > 0:
            print(f"Video file size: {os.path.getsize(final_video_path) / (1024*1024):.2f} MB")
        else:
            raise FileNotFoundError("Final video file was not created or is empty")
        
        return final_video_path
        
    except Exception as e:
        print(f"❌ Error during video generation: {e}")
        raise
    finally:
        if CLEANUP_TEMP_FILES:
            cleanup_temp_files(temp_files_to_clean)

def create_video_ffmpeg_optimized(total_video_duration, progress_tracker=None):
    """Main function to create video with all optimizations using ffmpeg-python"""
    
    print(f"🚀 Starting optimized video creation for {total_video_duration} seconds...")
    start_time = time.time()
    
    try:
        # Debug directory paths
        print(f"🔍 Directory paths:")
        print(f"   BASE_DIR: {BASE_DIR}")
        print(f"   MUSIC_FOLDER: {MUSIC_FOLDER}")
        print(f"   IMAGES_FOLDER: {IMAGES_FOLDER}")
        print(f"   FINAL_VIDEOS_FOLDER: {FINAL_VIDEOS_FOLDER}")
        print(f"   TEMP_FILES_FOLDER: {TEMP_FILES_FOLDER}")
        
        ensure_directory_exists(TEMP_FILES_FOLDER)
        ensure_directory_exists(FINAL_VIDEOS_FOLDER)
        
        # Verify directories exist and are writable
        print(f"🔍 Directory verification:")
        for dir_path, dir_name in [
            (MUSIC_FOLDER, "Music"),
            (IMAGES_FOLDER, "Images"), 
            (TEMP_FILES_FOLDER, "Temp Files"),
            (FINAL_VIDEOS_FOLDER, "Final Videos")
        ]:
            if os.path.exists(dir_path):
                try:
                    # Test if directory is writable
                    test_file = os.path.join(dir_path, "test_write.tmp")
                    with open(test_file, 'w') as f:
                        f.write("test")
                    os.remove(test_file)
                    print(f"   ✅ {dir_name}: {dir_path} (writable)")
                except Exception as e:
                    print(f"   ❌ {dir_name}: {dir_path} (not writable: {e})")
            else:
                print(f"   ❌ {dir_name}: {dir_path} (does not exist)")
        
        print("📁 Scanning for media files...")
        audio_files = get_supported_files(MUSIC_FOLDER, AUDIO_EXTENSIONS)
        image_files = get_supported_files(IMAGES_FOLDER, IMAGE_EXTENSIONS)
        
        if not audio_files:
            raise ValueError("No supported audio files found in the music folder")
        if not image_files:
            raise ValueError("No supported image files found in the images folder")
        
        print(f"✅ Found {len(audio_files)} audio files and {len(image_files)} image files")
        
        total_image_duration = len(image_files) * IMAGE_DURATION
        if total_image_duration < total_video_duration:
            print(f"⚠️  Warning: Image content ({total_image_duration}s) is shorter than requested duration ({total_video_duration}s)")
            total_video_duration = total_image_duration
        
        final_video_path = generate_video_ffmpeg(
            audio_files, 
            image_files, 
            FINAL_VIDEOS_FOLDER, 
            total_video_duration,
            progress_tracker
        )
        
        if not final_video_path or not os.path.exists(final_video_path) or os.path.getsize(final_video_path) == 0:
            raise ValueError("Video generation failed - no valid output file created")
        
        end_time = time.time()
        processing_time = end_time - start_time
        print(f"⏱️  Total processing time: {processing_time:.2f} seconds")
        print(f"📊 Processing speed: {total_video_duration/processing_time:.2f} seconds of video per second of processing")
        
        return final_video_path
        
    except Exception as e:
        print(f"❌ Video creation failed: {e}")
        import traceback
        print(f"Error details: {traceback.format_exc()}")
        raise

if __name__ == "__main__":
    progress_tracker = VideoProgressTracker()
    
    try:
        # Create a 5-minute (300 seconds) video
        create_video_ffmpeg_optimized(300, progress_tracker)
    except Exception as e:
        print(f"Error: {e}")