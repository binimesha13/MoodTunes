# MoodTunes
An AI-powered mood-based music recommender that detects a user's emotional state from natural language text input and generates a personalized playlist (English + Bollywood songs) — with an explanation of *why* each song was picked, and a feedback loop that learns from likes/skips.

##  Live Demo
https://binimesha13-moodtunes-music-mh73n1.streamlit.app/

##  Features
- Detects mood from user's text using NLP sentiment analysis (TextBlob)
- Classifies mood into: Happy, Sad, Energetic, Calm
- Recommends songs matched by valence & energy from a curated song database (English + Bollywood)
- Explains *why* each song was picked based on mood-matching features
- Feedback system (👍 Like / 👎 Skip) that logs preferences for future personalization
- Built with an interactive Streamlit UI

##  Tech Stack
- **Python**
- **Streamlit** – for the web app interface
- **TextBlob** – for NLP sentiment analysis
- **Pandas** – for data handling

## How to Run Locally

```bash
git clone https://github.com/binimesha13/MoodTunes.git
cd MoodTunes
pip install -r requirements.txt
streamlit run music.py
```

##  Project Structure

```
MoodTunes/
│
├── music.py            # Main application code
├── requirements.txt    # Python dependencies
├── feedback.csv        # Stores user like/skip feedback
└── README.md
```

##  Future Scope
- Selfie-based emotion detection using computer vision (DeepFace)
- Integration with Spotify API for real song playback
- Larger song database with real audio features (valence, energy, danceability)
- Improved recommendation using collaborative filtering based on feedback history

##  Author
Binimesha Naisargika- https://www.linkedin.com/in/binimesha-naisargika-26b176291/