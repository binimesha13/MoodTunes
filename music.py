import streamlit as st
from textblob import TextBlob
import pandas as pd
import random
import os
import csv

songs = [
  
    {"title": "Happy - Pharrell Williams", "mood": "happy", "energy": 0.9, "valence": 0.95},
    {"title": "Blinding Lights - The Weeknd", "mood": "happy", "energy": 0.85, "valence": 0.8},
    {"title": "Uptown Funk - Bruno Mars", "mood": "happy", "energy": 0.95, "valence": 0.9},
    {"title": "Can't Stop the Feeling - Justin Timberlake", "mood": "happy", "energy": 0.9, "valence": 0.92},

    {"title": "Gallan Goodiyaan - Dil Dhadakne Do", "mood": "happy", "energy": 0.9, "valence": 0.93},
    {"title": "London Thumakda - Queen", "mood": "happy", "energy": 0.92, "valence": 0.9},
    {"title": "Badtameez Dil - Yeh Jawaani Hai Deewani", "mood": "happy", "energy": 0.93, "valence": 0.88},
    {"title": "Nachde Ne Saare - Baar Baar Dekho", "mood": "happy", "energy": 0.88, "valence": 0.85},

    
    {"title": "Someone Like You - Adele", "mood": "sad", "energy": 0.2, "valence": 0.15},
    {"title": "Fix You - Coldplay", "mood": "sad", "energy": 0.25, "valence": 0.2},
    {"title": "Let Her Go - Passenger", "mood": "sad", "energy": 0.3, "valence": 0.25},
    {"title": "Skinny Love - Bon Iver", "mood": "sad", "energy": 0.15, "valence": 0.18},

    
    {"title": "Channa Mereya - Ae Dil Hai Mushkil", "mood": "sad", "energy": 0.2, "valence": 0.15},
    {"title": "Agar Tum Saath Ho - Tamasha", "mood": "sad", "energy": 0.18, "valence": 0.12},
    {"title": "Tum Hi Ho - Aashiqui 2", "mood": "sad", "energy": 0.22, "valence": 0.17},
    {"title": "Kabira - Yeh Jawaani Hai Deewani", "mood": "sad", "energy": 0.25, "valence": 0.2},

    
    {"title": "Eye of the Tiger - Survivor", "mood": "energetic", "energy": 0.98, "valence": 0.7},
    {"title": "Stronger - Kanye West", "mood": "energetic", "energy": 0.95, "valence": 0.65},
    {"title": "Levels - Avicii", "mood": "energetic", "energy": 0.97, "valence": 0.75},
    {"title": "Titanium - David Guetta", "mood": "energetic", "energy": 0.9, "valence": 0.68},

   
    {"title": "Zinda - Bhaag Milkha Bhaag", "mood": "energetic", "energy": 0.95, "valence": 0.72},
    {"title": "Malhari - Bajirao Mastani", "mood": "energetic", "energy": 0.96, "valence": 0.7},
    {"title": "Sultan Anthem - Sultan", "mood": "energetic", "energy": 0.93, "valence": 0.68},
    {"title": "Apna Time Aayega - Gully Boy", "mood": "energetic", "energy": 0.94, "valence": 0.75},

   
    {"title": "Weightless - Marconi Union", "mood": "calm", "energy": 0.1, "valence": 0.5},
    {"title": "Clair de Lune - Debussy", "mood": "calm", "energy": 0.08, "valence": 0.55},
    {"title": "Breathe Me - Sia", "mood": "calm", "energy": 0.15, "valence": 0.4},
    {"title": "Holocene - Bon Iver", "mood": "calm", "energy": 0.12, "valence": 0.45},

    {"title": "Tum Se Hi - Jab We Met", "mood": "calm", "energy": 0.15, "valence": 0.5},
    {"title": "Ilahi - Yeh Jawaani Hai Deewani", "mood": "calm", "energy": 0.18, "valence": 0.55},
    {"title": "Phir Se Ud Chala - Rockstar", "mood": "calm", "energy": 0.12, "valence": 0.48},
    {"title": "Kun Faya Kun - Rockstar", "mood": "calm", "energy": 0.1, "valence": 0.45},
]
df_songs = pd.DataFrame(songs)

FEEDBACK_FILE = "feedback.csv"
if not os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "action"])


def detect_mood(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity      
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.4:
        mood = "happy"
    elif polarity < -0.3:
        mood = "sad"
    elif polarity >= 0 and subjectivity > 0.5:
        mood = "energetic"
    else:
        mood = "calm"

    return mood, polarity, subjectivity

def recommend_songs(mood, n=4):
    matched = df_songs[df_songs["mood"] == mood].copy()
    matched = matched.sort_values(by="valence", ascending=False)
    return matched.head(n)

def log_feedback(title, action):
    with open(FEEDBACK_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([title, action])

def get_liked_moods():
    if os.path.getsize(FEEDBACK_FILE) == 0:
        return {}
    fb = pd.read_csv(FEEDBACK_FILE)
    if fb.empty:
        return {}
    liked = fb[fb["action"] == "like"]
    liked_titles = liked["title"].tolist()
    liked_songs = df_songs[df_songs["title"].isin(liked_titles)]
    return liked_songs["mood"].value_counts().to_dict()


st.set_page_config(page_title="Mood-to-Music AI DJ", page_icon="🎧")
st.title("🎧 Mood-to-Music AI DJ")
st.write("Tell me how you're feeling, and I'll build you a playlist.")

user_text = st.text_area("How are you feeling right now?", placeholder="e.g. I had a great day, feeling super excited!")

if st.button("Generate Playlist"):
    if user_text.strip() == "":
        st.warning("Please write something about how you feel.")
    else:
        mood, polarity, subjectivity = detect_mood(user_text)
        st.subheader(f"Detected Mood: **{mood.upper()}**")
        st.caption(f"Sentiment Polarity: {polarity:.2f} | Subjectivity: {subjectivity:.2f}")

        recs = recommend_songs(mood)

        st.subheader("Your Playlist")
        for idx, row in recs.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{row['title']}**")
                st.caption(f"Why this song: matches '{mood}' mood — energy: {row['energy']}, valence: {row['valence']}")
            with col2:
                like_key = f"like_{idx}"
                skip_key = f"skip_{idx}"
                if st.button("👍 Like", key=like_key):
                    log_feedback(row['title'], "like")
                    st.success("Liked! I'll remember this.")
                if st.button("👎 Skip", key=skip_key):
                    log_feedback(row['title'], "skip")
                    st.info("Skipped. Noted.")

        st.divider()
        liked_moods = get_liked_moods()
        if liked_moods:
            st.subheader("📊 Your Learned Preferences")
            st.write("Based on your likes so far, you tend to enjoy:")
            st.bar_chart(pd.Series(liked_moods))

st.divider()
st.caption("Built with Python, TextBlob (NLP sentiment analysis), and Streamlit.")