# voice.py
import speech_recognition as sr
from pydub import AudioSegment
from pathlib import Path
import tempfile

def transcribe_audio(file_bytes: bytes, filename: str) -> str:
    """
    Accepts uploaded audio (mp3/wav/m4a). Uses Google Web Speech (no key needed).
    Returns transcript string or '' on failure.
    """
    try:
        suffix = Path(filename).suffix.lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_in:
            tmp_in.write(file_bytes)
            tmp_in.flush()
            tmp_in_path = Path(tmp_in.name)

        # Convert to wav if needed (SpeechRecognition prefers wav)
        wav_path = tmp_in_path
        if suffix != ".wav":
            audio = AudioSegment.from_file(tmp_in_path)
            wav_path = tmp_in_path.with_suffix(".wav")
            audio.export(wav_path, format="wav")

        r = sr.Recognizer()
        with sr.AudioFile(str(wav_path)) as source:
            audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data)
            return text
        except Exception:
            return ""
    except Exception:
        return ""
