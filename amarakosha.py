import os
import requests
from bs4 import BeautifulSoup
import time
import random
import traceback
from tqdm import tqdm

# Define the base URL
BASE_URL = "https://hrishikeshrt.github.io/audio_alignment/corpus/amarakosha/"

# Define the number of sargas for each kanda
KANDAS = {
    1: 10,
    2: 10,
    3: 5
}

# Define file paths
sentence_csv_file = "amarakosha_sentence_data.csv"
word_csv_file = "amarakosha_word_data.csv"
audio_directory = "amarakosha_audio"
log_file = "error_log.txt"

# Ensure required directories exist
os.makedirs(audio_directory, exist_ok=True)

# Ensure CSV files exist and have headers
if not os.path.exists(sentence_csv_file):
    with open(sentence_csv_file, "w", encoding="utf-8") as f:
        f.write("Kanda,Sarga,Sentence,Sentence Start,Sentence End\n")

if not os.path.exists(word_csv_file):
    with open(word_csv_file, "w", encoding="utf-8") as f:
        f.write("Kanda,Sarga,Word,Word Start,Word End\n")

# Logging function
def log_error(message):
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(message + "\n")
        log.write(traceback.format_exc() + "\n")

# Function to fetch URL with retries and rate limiting
MAX_RETRIES = 3

def fetch_url(url):
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                wait_time = 2 ** attempt + random.uniform(0, 1)
                log_error(f"Rate limit exceeded for {url}, retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
        except requests.RequestException as e:
            log_error(f"Request error for {url}: {e}")
        time.sleep(2)
    return None  # Return None if all retries fail

# Main scraping function
def scrape_data():
    for kanda, num_sargas in tqdm(KANDAS.items(), desc="Processing Kandas"):
        for sarga in tqdm(range(1, num_sargas + 1), desc=f"Processing Sargas for Kanda {kanda}", leave=False):
            url = f"{BASE_URL}{kanda}.{sarga}/"
            print(f"Scraping: {url}")

            response = fetch_url(url)
            if not response:
                log_error(f"Failed to fetch {url} after retries, skipping...")
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')

            # Download and save audio file
            audio_url = f"https://ia904603.us.archive.org/30/items/amarakosha_audio/{kanda}.{sarga}.mp3"
            audio_response = fetch_url(audio_url)

            kanda_sarga_audio_dir = os.path.join(audio_directory, str(kanda))
            os.makedirs(kanda_sarga_audio_dir, exist_ok=True)  # Ensure directory exists

            if audio_response:
                audio_path = os.path.join(kanda_sarga_audio_dir, f"{sarga}.mp3")
                with open(audio_path, "wb") as f:
                    f.write(audio_response.content)
            else:
                log_error(f"Failed to fetch audio from {audio_url}, skipping...")

            # Locate text container
            text_container = soup.find(id="text-container")
            if not text_container:
                log_error(f"No text-container found in {url}. Page content:\n{soup.prettify()[:500]}")
                continue
            
            # Extract sentences and words
            for sentence in tqdm(text_container.find_all(class_="sentence-unit"), desc=f"Processing Sentences for {kanda}.{sarga}", leave=False):
                try:
                    sentence_text = sentence.get_text(strip=True)
                    sentence_begin = sentence.get("data-begin", "")
                    sentence_end = sentence.get("data-end", "")

                    with open(sentence_csv_file, "a", encoding="utf-8") as f:
                        f.write(f"{kanda},{sarga},{sentence_text},{sentence_begin},{sentence_end}\n")
                
                    # Extract word units inside sentence
                    for word in sentence.find_all(class_="word-unit"):
                        try:
                            word_text = word.get_text(strip=True)
                            word_begin = word.get("data-begin", "")
                            word_end = word.get("data-end", "")

                            with open(word_csv_file, "a", encoding="utf-8") as f:
                                f.write(f"{kanda},{sarga},{word_text},{word_begin},{word_end}\n")
                        except Exception as e:
                            log_error(f"Error processing word in {url}: {e}")
                except Exception as e:
                    log_error(f"Error processing sentence in {url}: {e}")

            # Sleep to avoid excessive requests
            time.sleep(random.uniform(1, 3))

    print("Data scraping completed.")

# Run the scraper
scrape_data()
