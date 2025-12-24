import sqlite3
import os

# Step 1: Delete old database if it exists
if os.path.exists("songs.db"):
    os.remove("songs.db")
    print("🗑 Old database deleted.")

# Step 2: Create new database connection
conn = sqlite3.connect("songs.db")
cursor = conn.cursor()

# Step 3: Create table with URL column
cursor.execute("""
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    artist TEXT NOT NULL,
    mood TEXT NOT NULL,
    url TEXT NOT NULL
)
""")

# Step 4: Real songs with YouTube links
songs_with_links = [
    # Happy
    ("Happy", "Pharrell Williams", "happy", "https://www.youtube.com/watch?v=ZbZSe6N_BXs"),
    ("Can't Stop the Feeling!", "Justin Timberlake", "happy", "https://www.youtube.com/watch?v=ru0K8uYEZWw"),
    ("Good as Hell", "Lizzo", "happy", "https://www.youtube.com/watch?v=vuq-VAiW9kw"),
    ("Walking on Sunshine", "Katrina & The Waves", "happy", "https://www.youtube.com/watch?v=iPUmE-tne5U"),
    ("Shake It Off", "Taylor Swift", "happy", "https://www.youtube.com/watch?v=nfWlot6h_JM"),

    # Sad
    ("Someone Like You", "Adele", "sad", "https://www.youtube.com/watch?v=hLQl3WQQoQ0"),
    ("Fix You", "Coldplay", "sad", "https://www.youtube.com/watch?v=k4V3Mo61fJM"),
    ("Let Her Go", "Passenger", "sad", "https://www.youtube.com/watch?v=RBumgq5yVrA"),
    ("Say Something", "A Great Big World", "sad", "https://www.youtube.com/watch?v=-2U0Ivkn2Ds"),
    ("The Night We Met", "Lord Huron", "sad", "https://www.youtube.com/watch?v=KtlgYxa6BMU"),

    # Neutral
    ("Shape of You", "Ed Sheeran", "neutral", "https://www.youtube.com/watch?v=JGwWNGJdvx8"),
    ("Counting Stars", "OneRepublic", "neutral", "https://www.youtube.com/watch?v=hT_nvWreIhg"),
    ("Blinding Lights", "The Weeknd", "neutral", "https://www.youtube.com/watch?v=4NRXx6U8ABQ"),
    ("Viva La Vida", "Coldplay", "neutral", "https://www.youtube.com/watch?v=dvgZkm1xWPE"),
    ("Adventure of a Lifetime", "Coldplay", "neutral", "https://www.youtube.com/watch?v=QtXby3twMmI")
]

# Step 5: Insert songs
cursor.executemany("INSERT INTO songs (name, artist, mood, url) VALUES (?, ?, ?, ?)", songs_with_links)

# Step 6: Commit changes and close
conn.commit()
conn.close()

# Step 7: Print inserted songs
print("✅ New database created with the following songs:")
for song in songs_with_links:
    print(f" - {song[0]} by {song[1]} ({song[2]})")
