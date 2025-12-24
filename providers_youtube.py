# providers_youtube.py
import urllib.parse

def youtube_search_link(query: str) -> str:
    base = "https://www.youtube.com/results?search_query="
    return base + urllib.parse.quote_plus(query)

def tracks_from_db_rows(rows):
    """
    Convert DB rows to unified track dicts (title, artist, url, preview_url=None).
    If a row has no url, we provide a YouTube search link for the title+artist.
    """
    results = []
    for r in rows:
        title, artist, mood, url = r["title"], r["artist"], r["mood"], r["url"]
        if not url:
            url = youtube_search_link(f"{title} {artist}")
        results.append({"title": title, "artist": artist, "url": url, "preview_url": None})
    return results

