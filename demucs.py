import os
import shutil
import subprocess
from tqdm import tqdm


input_items = [
    "amarakosha_audio/",
    "ashtadhyayi_audio/",  
    "ramayana_audio/",
]  

output_root = "demucs"  
temp_dir = "demucs_temp"  


def get_audio_files():
    audio_files = []
    
    for item in input_items:
        if os.path.isdir(item):  
            for dirpath, _, filenames in os.walk(item):
                for file in filenames:
                    if file.endswith((".mp3", ".wav", ".flac", ".m4a", ".ogg")):
                        audio_files.append(os.path.join(dirpath, file))
        elif os.path.isfile(item):  
            if item.endswith((".mp3", ".wav", ".flac", ".m4a", ".ogg")):
                audio_files.append(item)

    return audio_files


def process_single_audio(input_audio):
    
    root_dir = next((d for d in input_items if input_audio.startswith(d)), None) or os.path.dirname(input_audio)
    relative_path = os.path.relpath(input_audio, root_dir)  
    track_name = os.path.splitext(os.path.basename(input_audio))[0]  

    
    output_dir = os.path.join(output_root, os.path.dirname(relative_path))  
    final_output = os.path.join(output_dir, f"{track_name}.wav")  

    
    if os.path.exists(final_output):
        return f"✅ Already exists: {final_output}"

    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    
    tqdm.write(f"🎵 Processing: {input_audio}")

    with tqdm(total=100, desc=f"Extracting {track_name}", unit="%", dynamic_ncols=True) as pbar:
        process = subprocess.Popen(
            ["demucs", "--two-stems=vocals", "-o", temp_dir, input_audio],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        
        for line in process.stdout:
            if "Processed" in line:
                pbar.update(20)  

        process.wait()
        pbar.update(100 - pbar.n)  

    
    demucs_model_dir = os.path.join(temp_dir, "htdemucs")
    vocals_path = os.path.join(demucs_model_dir, track_name, "vocals.wav")

    
    if os.path.exists(vocals_path):
        shutil.move(vocals_path, final_output)
        result = f"✅ Saved vocals: {final_output}"
    else:
        result = f"❌ Error: Vocals not found for {input_audio}"

    
    shutil.rmtree(temp_dir, ignore_errors=True)

    return result


def process_audio_files():
    audio_files = get_audio_files()
    
    if not audio_files:
        print("❌ No audio files found in the given directories!")
        return

    print(f"🔍 Found {len(audio_files)} audio files. Processing...\n")

    for audio in tqdm(audio_files, desc="Overall Progress", unit="file"):
        result = process_single_audio(audio)
        tqdm.write(result)  


process_audio_files()
