# app.py
import os
import io
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from db import init_db, fetch_songs_by_mood, insert_mood, bulk_add_songs, delete_all_songs
from db import add_song, get_mood_history
from auth import signup, login
from mood import detect_mood
from voice import transcribe_audio
from providers_spotify import search_tracks_by_mood
from providers_youtube import tracks_from_db_rows, youtube_search_link

st.set_page_config(page_title="Mood Music Pro", page_icon="🎧", layout="wide")

# ---------- Init DB once ----------
init_db()

# ---------- Session State ----------
if "user" not in st.session_state:
    st.session_state.user = None
if "username" not in st.session_state:
    st.session_state.username = None

# ---------- Auth Sidebar ----------
with st.sidebar:
    st.header("👤 Account")
    if st.session_state.user is None:
        tab_login, tab_signup = st.tabs(["Login", "Sign up"])
        with tab_login:
            u = st.text_input("Username", key="login_user")
            p = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login"):
                ok, data = login(u, p)
                if ok:
                    st.session_state.user = data["id"]
                    st.session_state.username = data["username"]
                    st.success(f"Welcome, {data['username']}!")
                else:
                    st.error(data)
        with tab_signup:
            u2 = st.text_input("New username", key="su_user")
            p2 = st.text_input("New password", type="password", key="su_pass")
            if st.button("Create account"):
                ok, msg = signup(u2, p2)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
    else:
        st.write(f"Logged in as **{st.session_state.username}**")
        if st.button("Log out"):
            st.session_state.user = None
            st.session_state.username = None
            st.rerun()

st.title("🎧 Mood-Based Music Playlist (Pro)")

if st.session_state.user is None:
    st.info("Please log in or sign up to continue.")
    st.stop()

# ---------- Input: text or voice ----------
colA, colB = st.columns([2,1])
with colA:
    st.subheader("Tell me how you feel")
    user_text = st.text_input("Type here:", placeholder="e.g., I'm feeling pumped for my workout!")
    upl = st.file_uploader("…or upload a short voice note (mp3/wav/m4a)", type=["mp3","wav","m4a"])
    if upl is not None and not user_text.strip():
        with st.spinner("Transcribing audio…"):
            text_from_audio = transcribe_audio(upl.read(), upl.name)
        if text_from_audio:
            st.success(f"Transcribed: “{text_from_audio}”")
            user_text = text_from_audio
        else:
            st.warning("Couldn’t transcribe this audio. Try a clearer clip or type your mood.")
with colB:
    energy = st.selectbox("Energy tweak", ["Auto","Relax","Moderate","Hype"])

# ---------- Detect mood ----------
if st.button("Generate Playlist", use_container_width=True):
    mood = detect_mood(user_text)
    # small manual tweak
    if energy == "Relax" and mood in {"energetic","happy"}:
        mood = "calm" if mood == "energetic" else "neutral"
    if energy == "Hype" and mood in {"neutral","calm"}:
        mood = "energetic"

    insert_mood(st.session_state.user, user_text, mood)
    st.session_state["last_mood"] = mood

if "last_mood" in st.session_state:
    mood = st.session_state["last_mood"]
    st.success(f"Detected mood: **{mood}**")

    # ---------- Tracks from DB ----------
    db_rows = fetch_songs_by_mood(mood, limit=50)
    db_tracks = tracks_from_db_rows(db_rows)

    # ---------- Optional Spotify ----------
    sp_tracks = search_tracks_by_mood(mood, limit=10)

    # ---------- Fallback to YouTube search if empty ----------
    results = db_tracks[:]
    if not results and not sp_tracks:
        # show some ready search links (works without keys)
        st.info("No local songs found. Showing YouTube search results instead.")
        st.markdown(f"[Open YouTube for **{mood}**]( {youtube_search_link(mood + ' music playlist')} )")

    # ---------- UI: Show tracks ----------
    # ---------- UI: Show tracks ----------
    if results:
        st.subheader("🎵 From your Library")
        for t in results:
            st.markdown(f"- [{t['title']} — {t['artist']}]({t['url']})")
    if sp_tracks:
        st.subheader("🟢 Spotify suggestions")
        for t in sp_tracks:
            line = f"- [{t['title']} — {t['artist']}]({t['url']})"
            if t["preview_url"]:
                st.audio(t["preview_url"])
            st.markdown(line)


# ---------- Admin / Data entry ----------
st.divider()
st.subheader("📥 Add songs to your Library")
with st.expander("Quick actions"):
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Seed 5 songs / mood (YouTube)", help="Adds demo songs for happy/sad/neutral/calm/energetic"):
            demo = [
                # happy
                ("Happy","Pharrell Williams","happy","https://www.youtube.com/watch?v=ZbZSe6N_BXs"),
                ("Can't Stop the Feeling!","Justin Timberlake","happy","https://www.youtube.com/watch?v=ru0K8uYEZWw"),
                ("Walking on Sunshine","Katrina & The Waves","happy","https://www.youtube.com/watch?v=iPUmE-tne5U"),
                ("Good as Hell","Lizzo","happy","https://www.youtube.com/watch?v=vuq-VAiW9kw"),
                ("Uptown Funk","Mark Ronson, Bruno Mars","happy","https://www.youtube.com/watch?v=OPf0YbXqDm0"),
                # sad
                ("Someone Like You","Adele","sad","https://www.youtube.com/watch?v=hLQl3WQQoQ0"),
                ("Fix You","Coldplay","sad","https://www.youtube.com/watch?v=k4V3Mo61fJM"),
                ("Let Her Go","Passenger","sad","https://www.youtube.com/watch?v=RBumgq5yVrA"),
                ("Say Something","A Great Big World","sad","https://www.youtube.com/watch?v=-2U0Ivkn2Ds"),
                ("The Night We Met","Lord Huron","sad","https://www.youtube.com/watch?v=KtlgYxa6BMU"),
                # neutral
                ("Shape of You","Ed Sheeran","neutral","https://www.youtube.com/watch?v=JGwWNGJdvx8"),
                ("Counting Stars","OneRepublic","neutral","https://www.youtube.com/watch?v=hT_nvWreIhg"),
                ("Blinding Lights","The Weeknd","neutral","https://www.youtube.com/watch?v=4NRXx6U8ABQ"),
                ("Viva La Vida","Coldplay","neutral","https://www.youtube.com/watch?v=dvgZkm1xWPE"),
                ("Levitating","Dua Lipa","neutral","https://www.youtube.com/watch?v=TUVcZfQe-Kw"),
                # calm
                ("Weightless","Marconi Union","calm","https://www.youtube.com/watch?v=UfcAVejslrU"),
                ("River Flows In You","Yiruma","calm","https://www.youtube.com/watch?v=7maJOI3QMu0"),
                ("Clair de Lune","Debussy","calm","https://www.youtube.com/watch?v=CvFH_6DNRCY"),
                ("Nocturne Op.9 No.2","Chopin","calm","https://www.youtube.com/watch?v=9E6b3swbnWg"),
                ("Nuvole Bianche","Einaudi","calm","https://www.youtube.com/watch?v=kcihcYEOeic"),
                # energetic
                ("Believer","Imagine Dragons","energetic","https://www.youtube.com/watch?v=7wtfhZwyrcc"),
                ("Titanium","David Guetta, Sia","energetic","https://www.youtube.com/watch?v=JRfuAukYTKg"),
                ("Stronger","Kanye West","energetic","https://www.youtube.com/watch?v=PsO6ZnUZI0g"),
                ("Can't Hold Us","Macklemore & Ryan Lewis","energetic","https://www.youtube.com/watch?v=2zNSgSzhBfM"),
                ("Power","Little Mix","energetic","https://www.youtube.com/watch?v=UuCq8mtK8Jg"),
            ]
            delete_all_songs()
            bulk_add_songs(demo)
            st.success("Seeded 25 demo songs!")
    with c2:
        st.write("")
    with c3:
        st.write("")

cA, cB = st.columns([2,2])
with cA:
    with st.form("manual_add"):
        t = st.text_input("Title")
        a = st.text_input("Artist")
        m = st.selectbox("Mood", ["happy","sad","neutral","calm","energetic"])
        u = st.text_input("URL (YouTube/Spotify, optional)")
        if st.form_submit_button("Add song"):
            if t and a and m:
                add_song(t, a, m, u if u else None)
                st.success("Song added.")

with cB:
    st.write("Upload CSV: columns = title,artist,mood,url")
    csv = st.file_uploader("Choose CSV", type=["csv"], key="csv_up")
    if csv is not None:
        try:
            df = pd.read_csv(csv)
            need_cols = {"title","artist","mood"}
            if not need_cols.issubset(set(map(str.lower, df.columns))):
                st.error("CSV must have columns: title, artist, mood [, url]")
            else:
                # Normalize columns
                cols = {c.lower(): c for c in df.columns}
                rows = []
                for _, r in df.iterrows():
                    title = r[cols["title"]]
                    artist = r[cols["artist"]]
                    mood = str(r[cols["mood"]]).lower()
                    url = r[cols["url"]] if "url" in cols else None
                    rows.append((title, artist, mood, url))
                bulk_add_songs(rows)
                st.success(f"Imported {len(rows)} songs.")
        except Exception as e:
            st.error(f"CSV error: {e}")

# ---------- Analytics ----------
st.divider()
st.subheader("📊 Mood analytics")
hist = get_mood_history(st.session_state.user, limit=5000)
if hist:
    df = pd.DataFrame([{"mood": r["detected_mood"], "created_at": pd.to_datetime(r["created_at"])} for r in hist])
    # weekly
    df["week"] = df["created_at"].dt.to_period("W").dt.start_time
    df["month"] = df["created_at"].dt.to_period("M").dt.start_time

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Weekly mood counts**")
        weekly = df.groupby(["week","mood"]).size().unstack(fill_value=0)
        fig1, ax1 = plt.subplots()
        weekly.plot(kind="bar", ax=ax1)
        ax1.set_ylabel("Count")
        st.pyplot(fig1)
    with col2:
        st.markdown("**Monthly mood counts**")
        monthly = df.groupby(["month","mood"]).size().unstack(fill_value=0)
        fig2, ax2 = plt.subplots()
        monthly.plot(kind="bar", ax=ax2)
        ax2.set_ylabel("Count")
        st.pyplot(fig2)
else:
    st.info("No mood history yet. Generate a playlist to start building analytics.")
