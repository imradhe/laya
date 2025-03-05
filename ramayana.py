import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm

# Define the base URL
BASE_URL = "https://hrishikeshrt.github.io/audio_alignment/corpus/ramayana/"

# Define the number of sargas for each kanda
KANDAS = {
    1: 77,
    2: 119,
    3: 75,
    4: 67,
    5: 68,
    6: 128
}

# Open CSV files for writing incrementally
sentence_csv_file = "ramayana_sentence_data.csv"
word_csv_file = "ramayana_word_data.csv"
log_file = "error_log.txt"

with open(sentence_csv_file, "w", encoding="utf-8") as f:
    f.write("Kanda,Sarga,Sentence,Sentence Start,Sentence End\n")

with open(word_csv_file, "w", encoding="utf-8") as f:
    f.write("Kanda,Sarga,Word,Word Start,Word End\n")

def log_error(message):
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(message + "\n")

# Function to fetch and parse data
def scrape_data():
    for kanda, num_sargas in tqdm(KANDAS.items(), desc="Processing Kandas"):
        for sarga in tqdm(range(1, num_sargas + 1), desc=f"Processing Sargas for Kanda {kanda}", leave=False):
            sarga_str = f"{sarga:03d}"  # Format sarga as three-digit
            url = f"{BASE_URL}{kanda}.{sarga_str}/"
            print(f"Scraping: {url}")
            
            try:
                response = requests.get(url)
                if response.status_code != 200:
                    log_error(f"Failed to fetch {url}, skipping...")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                text_container = soup.find(id="text-container")
                if not text_container:
                    log_error(f"No text-container found in {url}")
                    continue
                
                # Extract sentence and word data
                for sentence in tqdm(text_container.find_all(class_="sentence-unit"), desc=f"Processing Sentences for {kanda}.{sarga_str}", leave=False):
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
            
            except Exception as e:
                log_error(f"Error processing {url}: {e}")
            
            # Sleep to avoid excessive requests
            time.sleep(1)
    print("Data scraping completed.")

# Run the scraper
scrape_data()