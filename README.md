# Laya – Audio & Text Alignment Tool

Laya is a lightweight browser-based tool built to align audio with word-level text for Sanskrit shlokas and other structured text, such as epics like the Ramayana. It supports manual timestamping, flagging, and transcript export — useful for training Text-to-Speech (TTS) models and precise sloka playback experiences (e.g., in Smruthi or Swara TTS).

⸻

✨ Features
	•	🎧 Audio Playback with Visual Sync

	•	Highlighted line follows audio playback in real-time.

	•	🧠 Manual Timestamping & Syncing

	•	Assign timestamps with keyboard (↓ and ↑)

	•	Adjust timestamps with precision (←/→)

	•	🎛️ Transcript Editing

	•	Add (Alt + Enter) and delete (Alt + Backspace) lines

	•	Update timestamps directly via playback

	•	🚩 Flagging Mechanism

	•	Mark lines with issues like mispronunciation or low volume

	•	Add reviewer comments

	•	📝 Export

	•	Download transcript as CSV with timestamps, flags, and comments

	•	🗂️ Kanda & Sarga Organization
	
	•	Load audio and transcript data by Kanda and Sarga divisions

⸻

⌨️ Keyboard Shortcuts

Shortcut	Action
Shift + Space	Play / Pause
↓ (Down Arrow)	Assign current time to next line
↑ (Up Arrow)	Reset time for current line
← / →	Adjust time by ±250ms
Shift + ← / →	Seek audio by ±1 second
Alt + Enter	Add line below current
Alt + Backspace	Delete current line (with confirm)



⸻

📦 Folder Structure

SwaraSangraha/
├── ramayana2/
│   ├── audio/            # Audio files organized as /Kanda/Sarga.mp3
│   └── word_data.json    # Input transcript JSON



⸻

🛠️ Setup & Usage

1. Serve Locally

You can open index.html directly in a browser, or serve via:

npx serve
# or
python3 -m http.server

2. Data Format (JSON)

word_data.json should be structured as:

[
  {
    "Kanda": "1",
    "Sarga": "1",
    "Word": "धर्मक्षेत्रे",
    "Word Start": "0.42"
  },
  ...
]

3. Audio Format

MP3 audio files should be placed in:

SwaraSangraha/ramayana2/audio/<Kanda>/<Sarga>.mp3



⸻

🧾 Export Format

Exported transcript.csv includes:

start,sentence,flags,comment
00:00:42,"धर्मक्षेत्रे","mispronunciation;low_volume","Needs re-recording"
...



⸻

🔍 Future Enhancements
	•	Auto-save to DB via API
	•	Forced alignment suggestions as initial timestamp
	•	Multi-speaker or layered annotation support
	•	Integration with Smruthi platform for preview/playback

⸻

🤝 Contributing

Feel free to fork and enhance! Submit issues or pull requests for bugs, UX suggestions, or new features.

⸻

🧠 Inspiration

Built for Swara TTS and Smruthi, to preserve and align sacred texts with accurate timing, pronunciation, and structure. Inspired by tools like Musixmatch for audio-word sync.

⸻