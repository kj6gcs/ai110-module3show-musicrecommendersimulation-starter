"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs

# Candidate personas from the Phase 2 design step (see README.md), saved here
# for later stress-testing against the recommender.
INTENSE_ROCK_PROFILE = {
    "genre": "rock",
    "mood": "intense",
    "tempo_bpm": 140,
    "valence": 0.50,
    "danceability": 0.55,
    "likes_acoustic": False,
}

CHILL_LOFI_PROFILE = {
    "genre": "lofi",
    "mood": "chill",
    "tempo_bpm": 75,
    "valence": 0.58,
    "danceability": 0.60,
    "likes_acoustic": True,
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "tempo_bpm": 120}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
