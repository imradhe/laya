import os
from mutagen import File
from tqdm import tqdm

# Base directory containing subdirectories with audio files
base_dir = "audio"

def get_audio_files(directory):
    """Recursively fetch all audio files from the directory and its subdirectories."""
    audio_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".mp3", ".wav", ".ogg")):  # Supported formats
                audio_files.append(os.path.join(root, file))
    return audio_files

def get_total_audio_duration(audio_files):
    """Calculate the total duration of all audio files from metadata."""
    total_duration = 0  # Total duration in seconds

    for file_path in tqdm(audio_files, desc="Processing Audio Files", unit="file"):
        try:
            audio = File(file_path)  # Detect format & read metadata
            if audio and audio.info:
                total_duration += audio.info.length  # Get duration in seconds
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return total_duration

# Fetch all audio files
audio_files = get_audio_files(base_dir)

# Calculate total duration
total_seconds = get_total_audio_duration(audio_files)

# Convert seconds to HH:MM:SS format
hours = int(total_seconds // 3600)
minutes = int((total_seconds % 3600) // 60)
seconds = int(total_seconds % 60)

print(f"\nTotal audio duration: {hours}h {minutes}m {seconds}s ({total_seconds:.2f} seconds)")
