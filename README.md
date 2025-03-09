# Project README

## Overview

This project involves processing and extracting data from various Sanskrit texts and audios and compile it as `SwaraSangraha`, ***A Sanskrit Chanting-style Speech Dataset***. 


## SwaraSangraha (स्वरसंग्रह)
1. [Amarakosha (अमरकोषः)](SwaraSangraha/amarakosha/)
1. [Ashtadhyayi (अष्टाध्यायी)](SwaraSangraha/ashtadhyayi/)
1. [Meghaduta (मेघदूतम्)](SwaraSangraha/meghaduta/)
1. [Valmiki Ramayana (वाल्मीकि रामायण)](SwaraSangraha/ramayana/)
1. [TarkaSangraga (तर्कसंग्रह)](SwaraSangraha/tarkasangraha/)
1. [Patanjali Yoga Sutrani (पातञ्जलयोगसूत्राणि) ](SwaraSangraha/yogasutra/)

## Data Collection & Processing
It includes modules for:

- **Web Scraping** of Sanskrit texts
- **Computing Total Duration of Audio Files**
- **Demucs-based Speech Separation**

## Directory Structure

```
📁 code
  📁 processing
    📄 demucs.py         # Demucs-based audio separation
    📄 duration.py       # Computes duration of audio files
  📁 scraping
    📄 amarakosha.py     # Scrapes Amarakosha text & audio
    📄 ashtadhyayi.py    # Scrapes Ashtadhyayi text & audio
    📄 meghaduta.py      # Scrapes Meghaduta text & audio
    📄 ramayana.py       # Scrapes Ramayana text & audio
    📄 tarkasangraha.py  # Scrapes Tarkasangraha text & audio
    📄 yogasutra.py      # Scrapes Yogasutra text & audio
  📁 test               # Directory for test files

📁 demucs               # Output directory for processed audio
📁 demucs_temp          # Temporary files during Demucs processing
📁 SwaraSangraha        # Collection of scraped Sanskrit audio/text
📁 separated_audio      # Storage for separated audio components
```

## Installation

### Dependencies

Ensure you have the required dependencies installed:

```bash
pip install numpy pandas librosa mutagen tqdm beautifulsoup4 requests pydub
```

### Running the Scripts

#### 1. Scrape Sanskrit Text and Audio

```bash
python code/scraping/amarakosha.py
python code/scraping/ashtadhyayi.py
python code/scraping/meghaduta.py
python code/scraping/ramayana.py
python code/scraping/tarkasangraha.py
python code/scraping/yogasutra.py
```

#### 2. Compute Total Duration of Audio Files

```bash
python code/processing/duration.py
```

#### 3. Run Demucs for Speech Separation

```bash
python code/processing/demucs.py
```

## Notes

- Ensure you have access to the internet while running the scraping scripts.
- Errors and warnings will be logged in `error_log.txt`.

---
