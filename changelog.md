# Change Log

### Substantial Changes to Starter Code

## 2026-07-09

- Removed the `energy` feature from the recommender entirely: dropped the `energy` column from `data/songs.csv`, removed `energy` from `Song` and `target_energy` from `UserProfile` in `src/recommender.py`, and updated the sample `user_prefs` in `src/main.py` to use `tempo_bpm` instead.
  - Reasoning: `energy` conflated a fixed song attribute with something that's really a subjective, moment-to-moment judgment call by the listener (their current mental/physical state), so it didn't belong as a static property of a `Song`.
  - Updated `tests/test_recommender.py` to match the new feature set (`genre`, `mood`, `tempo_bpm`, `valence`, `danceability`, `acousticness`).
  - Note: `README.md` and `model_card.md` were intentionally left unchanged (still reference `energy` in their example prompts) to preserve CodePath's original grading phrasing.
