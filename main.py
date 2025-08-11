import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
from functions.mixCreate import create_video_ffmpeg_optimized
from automate.auto import automate_process
import time
import threading
import json
import logging
from datetime import datetime
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)

class AutomationController:
    """Controls automation state and provides thread-safe operations"""
    def __init__(self):
        self.running = False
        self.paused = False
        self.current_status = "Ready"
        self.progress = 0
        self.lock = threading.Lock()
        self.automation_thread = None
        self.cycle_count = 0
        self.start_time = None
        
    def start(self):
        with self.lock:
            self.running = True
            self.paused = False
            self.cycle_count = 0
            self.start_time = datetime.now()
            logging.info("Automation started")
    
    def stop(self):
        with self.lock:
            self.running = False
            self.paused = False
            logging.info("Automation stopped")
    
    def pause(self):
        with self.lock:
            self.paused = True
            logging.info("Automation paused")
    
    def resume(self):
        with self.lock:
            self.paused = False
            logging.info("Automation resumed")
    
    def update_status(self, status, progress=None):
        with self.lock:
            self.current_status = status
            if progress is not None:
                self.progress = progress
    
    def get_status(self):
        with self.lock:
            return {
                'running': self.running,
                'paused': self.paused,
                'status': self.current_status,
                'progress': self.progress,
                'cycle_count': self.cycle_count,
                'start_time': self.start_time
            }

class VideoProgressTracker:
    """Thread-safe progress tracker for video processing"""
    def __init__(self, controller):
        self.controller = controller
    
    def update(self, progress, status):
        self.controller.update_status(status, progress)

# Global variables
video_duration = None
automation_controller = AutomationController()

# Configuration
CONFIG_FILE = "automation_config.json"
DEFAULT_CONFIG = {
    "channel_name": "SleepRelaxAndMeditates",
    "cycle_delay": 30,
    "max_cycles": 10,
    "auto_cleanup": True,
    "file_size_limit_mb": 100,
    "supported_image_formats": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "supported_audio_formats": [".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"]
}

def load_config():
    """Load configuration from file or create default"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
        else:
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return DEFAULT_CONFIG

def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        logging.info("Configuration saved")
    except Exception as e:
        logging.error(f"Error saving config: {e}")

def check_disk_space(folder_path, required_mb=100):
    """Check if there's enough disk space"""
    try:
        total, used, free = shutil.disk_usage(folder_path)
        free_mb = free // (1024 * 1024)
        return free_mb >= required_mb
    except Exception as e:
        logging.warning(f"Could not check disk space: {e}")
        return True  # Assume OK if we can't check

def validate_file(file_path, max_size_mb=100):
    """Validate file size and format"""
    try:
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        if file_size_mb > max_size_mb:
            return False, f"File too large: {file_size_mb:.1f}MB > {max_size_mb}MB"
        
        return True, "OK"
    except Exception as e:
        return False, f"Validation error: {e}"

def safe_file_operation(operation, *args, **kwargs):
    """Safely execute file operations with error handling"""
    try:
        return operation(*args, **kwargs)
    except PermissionError:
        messagebox.showerror("Permission Error", "Access denied to file/folder")
        logging.error("Permission denied for file operation")
        return None
    except FileNotFoundError:
        messagebox.showerror("File Error", "File or folder not found")
        logging.error("File not found")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Operation failed: {str(e)}")
        logging.error(f"File operation failed: {e}")
        return None

def start_automation():
    """Start the automation process with validation"""
    global video_duration
    
    try:
        video_duration_input = entry_video_duration.get().strip()
        
        if not video_duration_input.isdigit() or int(video_duration_input) <= 0:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number for video duration.")
            return
        
        video_duration = int(video_duration_input)
        
        # Check disk space
        if not check_disk_space(".", 200):
            messagebox.showerror("Insufficient Space", "Not enough disk space for video creation (need at least 200MB)")
            return
        
        # Check if media files exist
        config = load_config()
        music_folder = os.path.join(os.getcwd(), "music")
        images_folder = os.path.join(os.getcwd(), "images")
        
        if not os.path.exists(music_folder) or not os.listdir(music_folder):
            messagebox.showerror("No Music", "Please upload some music files first.")
            return
        
        if not os.path.exists(images_folder) or not os.listdir(images_folder):
            messagebox.showerror("No Images", "Please upload some image files first.")
            return
        
        # Start automation
        automation_controller.start()
        update_ui_state()
        
        automation_thread = threading.Thread(
            target=start_video_generation_and_automation, 
            args=(config["channel_name"],),
            daemon=True
        )
        automation_thread.start()
        
        logging.info(f"Automation started for {video_duration} seconds")
        
    except Exception as e:
        logging.error(f"Error starting automation: {e}")
        messagebox.showerror("Error", f"Failed to start automation: {str(e)}")

def stop_automation():
    """Stop the automation process"""
    automation_controller.stop()
    update_ui_state()
    logging.info("Automation stopped by user")

def pause_automation():
    """Pause the automation process"""
    automation_controller.pause()
    update_ui_state()

def resume_automation():
    """Resume the automation process"""
    automation_controller.resume()
    update_ui_state()

def start_video_generation_and_automation(channel_name):
    """Controlled video generation and automation process"""
    config = load_config()
    max_cycles = config.get("max_cycles", 10)
    cycle_delay = config.get("cycle_delay", 30)
    
    try:
        while automation_controller.running and automation_controller.cycle_count < max_cycles:
            if automation_controller.paused:
                automation_controller.update_status("Paused", 0)
                time.sleep(1)
                continue
            
            automation_controller.update_status("Starting cycle...", 10)
            automation_controller.cycle_count += 1
            
            logging.info(f"Starting cycle {automation_controller.cycle_count}/{max_cycles}")
            
            # Check if still running after status update
            if not automation_controller.running:
                break
            
            automation_controller.update_status("Creating video...", 20)
            logging.info(f"Generating video for channel '{channel_name}' with duration {video_duration} seconds")
            
            # Create video with progress tracking
            progress_tracker = VideoProgressTracker(automation_controller)
            create_video_ffmpeg_optimized(video_duration, progress_tracker)
            
            if not automation_controller.running:
                break
            
            automation_controller.update_status("Starting automation...", 80)
            logging.info("Starting automation tasks...")
            success = automate_process(channel_name)
            
            if success:
                automation_controller.update_status("Cycle completed", 100)
                logging.info(f"Cycle {automation_controller.cycle_count} completed successfully")
            else:
                automation_controller.update_status("Automation failed", 0)
                logging.error(f"Cycle {automation_controller.cycle_count} failed")
                messagebox.showwarning("Automation Warning", f"Cycle {automation_controller.cycle_count} failed. Check logs for details.")
            
            if not automation_controller.running:
                break
            
            # Wait before next cycle
            automation_controller.update_status(f"Waiting {cycle_delay}s before next cycle...", 0)
            for i in range(cycle_delay):
                if not automation_controller.running:
                    break
                time.sleep(1)
        
        if automation_controller.cycle_count >= max_cycles:
            automation_controller.update_status("Maximum cycles reached", 100)
            logging.info(f"Automation completed after {max_cycles} cycles")
            messagebox.showinfo("Automation Complete", f"Automation completed after {max_cycles} cycles.")
        
        automation_controller.stop()
        update_ui_state()
        
    except Exception as e:
        logging.error(f"Error during automation: {e}")
        automation_controller.update_status(f"Error: {str(e)}", 0)
        messagebox.showerror("Automation Error", f"Automation failed: {str(e)}")
        automation_controller.stop()
        update_ui_state()

def update_ui_state():
    """Update UI elements based on automation state"""
    status = automation_controller.get_status()
    
    if status['running']:
        if status['paused']:
            button_start.config(state='normal', text='Resume', command=resume_automation)
            button_stop.config(state='normal', text='Stop')
            button_pause.config(state='disabled', text='Paused')
        else:
            button_start.config(state='disabled', text='Running', command=start_automation)
            button_stop.config(state='normal', text='Stop')
            button_pause.config(state='normal', text='Pause')
    else:
        button_start.config(state='normal', text='Start Automation')
        button_stop.config(state='disabled', text='Stop')
        button_pause.config(state='disabled', text='Pause')
    
    # Update status display
    status_text = f"Status: {status['status']}"
    if status['running']:
        status_text += f" | Cycles: {status['cycle_count']}"
        if status['start_time']:
            elapsed = datetime.now() - status['start_time']
            status_text += f" | Elapsed: {str(elapsed).split('.')[0]}"
    
    status_label.config(text=status_text)
    
    # Update progress bar
    if status['running'] and not status['paused']:
        progress_bar.start()
    else:
        progress_bar.stop()
    
    # Schedule next update
    if status['running']:
        root.after(1000, update_ui_state)

def upload_images():
    """Upload images with validation and progress feedback"""
    config = load_config()
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp;*.tiff;*.webp"), ("All Files", "*.*")]
    )
    
    if not file_paths:
        return
    
    images_folder = os.path.join(os.getcwd(), "images")
    safe_file_operation(os.makedirs, images_folder, exist_ok=True)
    
    successful_uploads = 0
    failed_uploads = 0
    
    for file_path in file_paths:
        try:
            # Validate file
            is_valid, message = validate_file(file_path, config["file_size_limit_mb"])
            if not is_valid:
                logging.warning(f"File validation failed for {file_path}: {message}")
                failed_uploads += 1
                continue
            
            # Copy file
            filename = os.path.basename(file_path)
            dest_path = os.path.join(images_folder, filename)
            shutil.copy2(file_path, dest_path)
            successful_uploads += 1
            logging.info(f"Image uploaded: {filename}")
            
        except Exception as e:
            logging.error(f"Failed to upload {os.path.basename(file_path)}: {e}")
            failed_uploads += 1
    
    # Show results
    if successful_uploads > 0:
        messagebox.showinfo("Upload Complete", 
                          f"Successfully uploaded {successful_uploads} images!")
    if failed_uploads > 0:
        messagebox.showwarning("Upload Issues", 
                             f"{failed_uploads} files failed to upload. Check logs for details.")

def upload_music():
    """Upload music files with validation and progress feedback"""
    config = load_config()
    file_paths = filedialog.askopenfilenames(
        title="Select Music Files",
        filetypes=[("Music Files", "*.mp3;*.wav;*.m4a;*.aac;*.flac;*.ogg"), ("All Files", "*.*")]
    )
    
    if not file_paths:
        return
    
    music_folder = os.path.join(os.getcwd(), "music")
    safe_file_operation(os.makedirs, music_folder, exist_ok=True)
    
    successful_uploads = 0
    failed_uploads = 0
    
    for file_path in file_paths:
        try:
            # Validate file
            is_valid, message = validate_file(file_path, config["file_size_limit_mb"])
            if not is_valid:
                logging.warning(f"File validation failed for {file_path}: {message}")
                failed_uploads += 1
                continue
            
            # Copy file
            filename = os.path.basename(file_path)
            dest_path = os.path.join(music_folder, filename)
            shutil.copy2(file_path, dest_path)
            successful_uploads += 1
            logging.info(f"Music uploaded: {filename}")
            
        except Exception as e:
            logging.error(f"Failed to upload {os.path.basename(file_path)}: {e}")
            failed_uploads += 1
    
    # Show results
    if successful_uploads > 0:
        messagebox.showinfo("Upload Complete", 
                          f"Successfully uploaded {successful_uploads} music files!")
    if failed_uploads > 0:
        messagebox.showwarning("Upload Issues", 
                             f"{failed_uploads} files failed to upload. Check logs for details.")

def delete_all_images():
    """Delete all images with confirmation"""
    if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete ALL images?"):
        return
    
    images_folder = os.path.join(os.getcwd(), "images")
    result = safe_file_operation(delete_folder_contents, images_folder, "images")
    if result:
        messagebox.showinfo("Success", "All images deleted successfully.")

def delete_all_music():
    """Delete all music files with confirmation"""
    if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete ALL music files?"):
        return
    
    music_folder = os.path.join(os.getcwd(), "music")
    result = safe_file_operation(delete_folder_contents, music_folder, "music files")
    if result:
        messagebox.showinfo("Success", "All music files deleted successfully.")

def delete_folder_contents(folder_path, item_name):
    """Safely delete all contents of a folder"""
    try:
        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logging.info(f"Deleted {item_name}: {file_name}")
        return True
    except Exception as e:
        logging.error(f"Failed to delete {item_name}: {e}")
        return False

def open_settings():
    """Open settings configuration window"""
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("500x400")
    settings_window.configure(bg='#f2f2f2')
    
    config = load_config()
    
    # Channel name
    tk.Label(settings_window, text="Channel Name:", bg='#f2f2f2').grid(row=0, column=0, pady=5, padx=5)
    channel_entry = tk.Entry(settings_window, width=30)
    channel_entry.insert(0, config["channel_name"])
    channel_entry.grid(row=0, column=1, pady=5, padx=5)
    
    # Cycle delay
    tk.Label(settings_window, text="Cycle Delay (seconds):", bg='#f2f2f2').grid(row=1, column=0, pady=5, padx=5)
    delay_entry = tk.Entry(settings_window, width=30)
    delay_entry.insert(0, str(config["cycle_delay"]))
    delay_entry.grid(row=1, column=1, pady=5, padx=5)
    
    # Max cycles
    tk.Label(settings_window, text="Max Cycles:", bg='#f2f2f2').grid(row=2, column=0, pady=5, padx=5)
    cycles_entry = tk.Entry(settings_window, width=30)
    cycles_entry.insert(0, str(config["max_cycles"]))
    cycles_entry.grid(row=2, column=1, pady=5, padx=5)
    
    # File size limit
    tk.Label(settings_window, text="File Size Limit (MB):", bg='#f2f2f2').grid(row=3, column=0, pady=5, padx=5)
    size_entry = tk.Entry(settings_window, width=30)
    size_entry.insert(0, str(config["file_size_limit_mb"]))
    size_entry.grid(row=3, column=1, pady=5, padx=5)
    
    def save_settings():
        try:
            new_config = config.copy()
            new_config["channel_name"] = channel_entry.get()
            new_config["cycle_delay"] = int(delay_entry.get())
            new_config["max_cycles"] = int(cycles_entry.get())
            new_config["file_size_limit_mb"] = int(size_entry.get())
            
            save_config(new_config)
            messagebox.showinfo("Success", "Settings saved successfully!")
            settings_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for numeric fields.")
    
    # Save button
    tk.Button(settings_window, text="Save Settings", command=save_settings, 
              bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold")).grid(row=4, column=0, columnspan=2, pady=20)

def show_system_info():
    """Display system information and resource usage"""
    try:
        # CPU and memory info
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('.')
        
        info_text = f"""System Information:
        
CPU Usage: {cpu_percent}%
Memory: {memory.percent}% used ({memory.used // (1024**3):.1f}GB / {memory.total // (1024**3):.1f}GB)
Disk: {disk.percent}% used ({disk.used // (1024**3):.1f}GB / {disk.total // (1024**3):.1f}GB)

Process Information:
Python Process: {psutil.Process().memory_info().rss // (1024**2):.1f}MB
Threads: {psutil.Process().num_threads()}
"""
        
        messagebox.showinfo("System Information", info_text)
    except Exception as e:
        messagebox.showerror("Error", f"Could not retrieve system information: {e}")

def cleanup_temp_files():
    """Clean up temporary files"""
    try:
        temp_folder = os.path.join(os.getcwd(), "tempFiles")
        if os.path.exists(temp_folder):
            for file_name in os.listdir(temp_folder):
                file_path = os.path.join(temp_folder, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logging.info(f"Cleaned up temp file: {file_name}")
        
        messagebox.showinfo("Cleanup Complete", "Temporary files cleaned up successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Cleanup failed: {e}")

# Load configuration
config = load_config()

# Create the main window
root = tk.Tk()
root.title("YouTube Video Upload Automation Tool - Enhanced")

# Set window size and make it resizable
root.geometry("900x700")
root.minsize(900, 700)

# Set the window background color
root.configure(bg='#f2f2f2')

# Create a canvas to enable scrolling
canvas = tk.Canvas(root, bg='#f2f2f2')
canvas.grid(row=0, column=0, sticky="nsew")

# Create a vertical scrollbar
vertical_scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
vertical_scrollbar.grid(row=0, column=1, sticky="ns")

# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=vertical_scrollbar.set)

# Create a frame inside the canvas to hold all widgets
frame = tk.Frame(canvas, bg='#f2f2f2')
canvas.create_window((0, 0), window=frame, anchor="nw")

# Title and status section
title_label = tk.Label(frame, text="Enhanced YouTube Video Automation Tool", 
                      font=("Helvetica", 18, "bold"), bg='#f2f2f2', fg="#333333")
title_label.grid(row=0, column=0, columnspan=3, pady=20)

# Status display
status_label = tk.Label(frame, text="Status: Ready", font=("Helvetica", 10), 
                       bg='#f2f2f2', fg="#666666")
status_label.grid(row=1, column=0, columnspan=3, pady=5)

# Progress bar
progress_bar = ttk.Progressbar(frame, mode='indeterminate', length=400)
progress_bar.grid(row=2, column=0, columnspan=3, pady=5)

# Video duration input
label_video_duration = tk.Label(frame, text="Video Duration (seconds):", 
                               font=("Helvetica", 12), bg='#f2f2f2', fg="#333333")
label_video_duration.grid(row=3, column=0, pady=10, padx=10, sticky="e")

entry_video_duration = tk.Entry(frame, font=("Helvetica", 14), width=20, bd=2, relief="solid")
entry_video_duration.grid(row=3, column=1, pady=10, sticky="w")
entry_video_duration.insert(0, "300")  # Default 5 minutes

# Control buttons
button_frame = tk.Frame(frame, bg='#f2f2f2')
button_frame.grid(row=4, column=0, columnspan=3, pady=20)

button_start = tk.Button(button_frame, text="Start Automation", 
                        font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", 
                        width=15, height=2, command=start_automation)
button_start.grid(row=0, column=0, padx=5)

button_pause = tk.Button(button_frame, text="Pause", 
                        font=("Helvetica", 12, "bold"), bg="#FF9800", fg="white", 
                        width=15, height=2, command=pause_automation, state='disabled')
button_pause.grid(row=0, column=1, padx=5)

button_stop = tk.Button(button_frame, text="Stop", 
                       font=("Helvetica", 12, "bold"), bg="#F44336", fg="white", 
                       width=15, height=2, command=stop_automation, state='disabled')
button_stop.grid(row=0, column=2, padx=5)

# File management buttons
file_frame = tk.Frame(frame, bg='#f2f2f2')
file_frame.grid(row=5, column=0, columnspan=3, pady=10)

button_upload_images = tk.Button(file_frame, text="Upload Images", 
                                font=("Helvetica", 12, "bold"), bg="#2196F3", fg="white", 
                                width=15, height=2, command=upload_images)
button_upload_images.grid(row=0, column=0, padx=5)

button_upload_music = tk.Button(file_frame, text="Upload Music", 
                               font=("Helvetica", 12, "bold"), bg="#FF5722", fg="white", 
                               width=15, height=2, command=upload_music)
button_upload_music.grid(row=0, column=1, padx=5)

button_delete_images = tk.Button(file_frame, text="Delete Images", 
                                font=("Helvetica", 12, "bold"), bg="#F44336", fg="white", 
                                width=15, height=2, command=delete_all_images)
button_delete_images.grid(row=0, column=2, padx=5)

button_delete_music = tk.Button(file_frame, text="Delete Music", 
                               font=("Helvetica", 12, "bold"), bg="#F44336", fg="white", 
                               width=15, height=2, command=delete_all_music)
button_delete_music.grid(row=1, column=0, padx=5, pady=5)

# Utility buttons
utility_frame = tk.Frame(frame, bg='#f2f2f2')
utility_frame.grid(row=6, column=0, columnspan=3, pady=10)

button_settings = tk.Button(utility_frame, text="Settings", 
                           font=("Helvetica", 10, "bold"), bg="#9C27B0", fg="white", 
                           width=12, height=1, command=open_settings)
button_settings.grid(row=0, column=0, padx=5)

button_system_info = tk.Button(utility_frame, text="System Info", 
                              font=("Helvetica", 10, "bold"), bg="#607D8B", fg="white", 
                              width=12, height=1, command=show_system_info)
button_system_info.grid(row=0, column=1, padx=5)

button_cleanup = tk.Button(utility_frame, text="Cleanup Temp", 
                          font=("Helvetica", 10, "bold"), bg="#795548", fg="white", 
                          width=12, height=1, command=cleanup_temp_files)
button_cleanup.grid(row=0, column=2, padx=5)

# Footer
footer_label = tk.Label(frame, text="Enhanced Automation Tool by Alex", 
                       font=("Helvetica", 10), bg='#f2f2f2', fg="#555555")
footer_label.grid(row=7, column=0, columnspan=3, pady=20)

# Configure grid weights
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3, weight=1)
frame.grid_rowconfigure(4, weight=1)
frame.grid_rowconfigure(5, weight=1)
frame.grid_rowconfigure(6, weight=1)
frame.grid_rowconfigure(7, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

# Update scrollregion
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Configure canvas grid weights
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Initialize UI state
update_ui_state()

# Run the main loop
if __name__ == "__main__":
    try:
        root.mainloop()
    except KeyboardInterrupt:
        logging.info("Application interrupted by user")
    except Exception as e:
        logging.error(f"Application error: {e}")
        messagebox.showerror("Critical Error", f"Application error: {e}")