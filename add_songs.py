import sqlite3

# Connect to DB
conn = sqlite3.connect('songs.db')
cursor = conn.cursor()

# 1. Add URL column if not exists
try:
    cursor.execute("ALTER TABLE songs ADD COLUMN url TEXT;")
except sqlite3.OperationalError:
    print("URL column already exists, skipping...")

# 2. Insert real songs for moods
songs_with_links = [
    # Happy Songs
    ("Happy", "Pharrell Williams", "happy", "https://www.youtube.com/watch?v=ZbZSe6N_BXs"),
    ("Shape of You", "Ed Sheeran", "happy", "https://www.youtube.com/watch?v=JGwWNGJdvx8"),
    ("Can't Stop the Feeling!", "Justin Timberlake", "happy", "https://www.youtube.com/watch?v=ru0K8uYEZWw"),
    ("Uptown Funk", "Mark Ronson ft. Bruno Mars", "happy", "https://www.youtube.com/watch?v=OPf0YbXqDm0"),
    ("Good as Hell", "Lizzo", "happy", "https://www.youtube.com/watch?v=vuq-VAiW9kw"),

    # Sad Songs
    ("Someone Like You", "Adele", "sad", "https://www.youtube.com/watch?v=hLQl3WQQoQ0"),
    ("Let Her Go", "Passenger", "sad", "https://www.youtube.com/watch?v=RBumgq5yVrA"),
    ("Fix You", "Coldplay", "sad", "https://www.youtube.com/watch?v=k4V3Mo61fJM"),
    ("All I Want", "Kodaline", "sad", "https://www.youtube.com/watch?v=mtf7hC17IBM"),
    ("Skinny Love", "Birdy", "sad", "https://www.youtube.com/watch?v=aNzCDt2eidg"),

    # Neutral / Chill Songs
    ("Stay", "The Kid LAROI & Justin Bieber", "neutral", "https://www.youtube.com/watch?v=kTJczUoc26U"),
    ("Memories", "Maroon 5", "neutral", "https://www.youtube.com/watch?v=SlPhMPnQ58k"),
    ("Counting Stars", "OneRepublic", "neutral", "https://www.youtube.com/watch?v=hT_nvWreIhg"),
    ("Blinding Lights", "The Weeknd", "neutral", "https://www.youtube.com/watch?v=4NRXx6U8ABQ"),
    ("Levitating", "Dua Lipa", "neutral", "https://www.youtube.com/watch?v=TUVcZfQe-Kw"),
]

# 3. Insert songs into DB
for name, artist, mood, url in songs_with_links:
    cursor.execute(
        "INSERT INTO songs (name, artist, mood, url) VALUES (?, ?, ?, ?)",
        (name, artist, mood, url)
    )

conn.commit()
conn.close()

print("✅ 5 songs for each mood added successfully!")
