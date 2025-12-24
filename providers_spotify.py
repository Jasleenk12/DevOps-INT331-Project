# providers_spotify.py
import os
from typing import List, Dict

def _client():
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    cid = os.getenv("SPOTIFY_CLIENT_ID")
    secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if not cid or not secret:
        return None
    auth_mgr = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(auth_manager=auth_mgr)
    return sp

def search_tracks_by_mood(mood: str, limit: int = 10) -> List[Dict]:
    """
    Returns: list of dicts: {title, artist, url, preview_url}
    If credentials missing, returns [] (caller can fallback).
    """
    sp = _client()
    if sp is None:
        return []
    # simple mapping mood->search query
    qmap = {
        "happy": "feel good pop",
        "sad": "sad acoustic",
        "calm": "lofi chill",
        "neutral": "soft pop",
        "energetic": "workout hits"
    }
    query = qmap.get(mood.lower(), mood)
    res = sp.search(q=query, type="track", limit=limit)
    out = []
    for item in res.get("tracks", {}).get("items", []):
        title = item["name"]
        artists = ", ".join([a["name"] for a in item["artists"]])
        url = item["external_urls"]["spotify"]
        preview = item.get("preview_url")  # can be None
        out.append({"title": title, "artist": artists, "url": url, "preview_url": preview})
    return out
