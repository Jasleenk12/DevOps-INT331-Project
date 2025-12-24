import sqlite3

conn = sqlite3.connect('songs.db')
cursor = conn.cursor()

cursor.execute("ALTER TABLE songs ADD COLUMN url TEXT;")

conn.commit()
conn.close()

print("URL column added successfully!")
