import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_tempo: float
    target_valence: float
    target_danceability: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv into a list of dicts, converting numeric fields to float/int."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def normalize_tempo(tempo_bpm: float, min_bpm: float = 40.0, max_bpm: float = 200.0) -> float:
    """Scales tempo_bpm to a 0-1 range so it's comparable to the other 0-1 features."""
    normalized = (tempo_bpm - min_bpm) / (max_bpm - min_bpm)
    return max(0.0, min(1.0, normalized))

def closeness_score(value: float, target: float, max_diff: float) -> float:
    """Rewards values close to a target rather than simply higher/lower ones."""
    diff = abs(value - target)
    return max(0.0, 1 - (diff / max_diff))

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user_prefs using the finalized Algorithm Recipe, returning (score, reasons)."""
    score = 0.0
    reasons = []

    if user_prefs.get("genre") == song["genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if user_prefs.get("mood") == song["mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    if "tempo_bpm" in user_prefs:
        tempo_points = closeness_score(
            normalize_tempo(song["tempo_bpm"]),
            normalize_tempo(user_prefs["tempo_bpm"]),
            max_diff=1.0,
        ) * 1.0
        score += tempo_points
        reasons.append(f"tempo closeness (+{tempo_points:.2f})")

    if "valence" in user_prefs:
        valence_points = closeness_score(song["valence"], user_prefs["valence"], max_diff=1.0) * 0.5
        score += valence_points
        reasons.append(f"valence closeness (+{valence_points:.2f})")

    if "danceability" in user_prefs:
        dance_points = closeness_score(song["danceability"], user_prefs["danceability"], max_diff=1.0) * 0.5
        score += dance_points
        reasons.append(f"danceability closeness (+{dance_points:.2f})")

    if "likes_acoustic" in user_prefs:
        song_is_acoustic = song["acousticness"] > 0.5
        if user_prefs["likes_acoustic"] == song_is_acoustic:
            score += 0.5
            reasons.append("acoustic alignment (+0.5)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song against user_prefs and returns the top k, highest score first."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    # sorted() returns a new list rather than mutating `scored` in place, which
    # matters here since `scored` isn't otherwise needed after ranking.
    ranked = sorted(scored, key=lambda entry: entry[1], reverse=True)
    return [(song, score, ", ".join(reasons)) for song, score, reasons in ranked[:k]]
