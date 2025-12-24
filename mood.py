# mood.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_an = SentimentIntensityAnalyzer()

KEY_HYPE = {"dance","party","hype","excited","pumped","workout","run","gym","energy"}
KEY_CALM = {"calm","relax","sleep","tired","chill","peace","meditate"}

def detect_mood(text: str) -> str:
    if not text or not text.strip():
        return "neutral"
    t = text.lower()
    scores = _an.polarity_scores(t)
    comp = scores["compound"]  # -1..1
    # simple arousal nudge
    if comp >= 0.5:
        if any(k in t for k in KEY_HYPE):
            return "energetic"
        return "happy"
    if comp <= -0.4:
        return "sad"
    if any(k in t for k in KEY_CALM):
        return "calm"
    if any(k in t for k in KEY_HYPE):
        return "energetic"
    return "neutral"
