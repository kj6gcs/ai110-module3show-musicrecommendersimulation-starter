# Change Log

### Substantial Changes to Starter Code

## 07-09-2026

- Removed the `energy` feature from the recommender entirely: dropped the `energy` column from `data/songs.csv`, removed `energy` from `Song` and `target_energy` from `UserProfile` in `src/recommender.py`, and updated the sample `user_prefs` in `src/main.py` to use `tempo_bpm` instead.
  - Reasoning: `energy` conflated a fixed song attribute with something that's really a subjective, moment-to-moment judgment call by the listener (their current mental/physical state), so it didn't belong as a static property of a `Song`.
  - Updated `tests/test_recommender.py` to match the new feature set (`genre`, `mood`, `tempo_bpm`, `valence`, `danceability`, `acousticness`).
  - Note: `README.md` and `model_card.md` were intentionally left unchanged (still reference `energy` in their example prompts) to preserve CodePath's original grading phrasing.

## 07-14-2026

- Documented the recommender's design in `README.md`'s "How The System Works" section: explained content-based vs. collaborative filtering in the context of this simulation, finalized the scoring weights (genre match +2.0, mood match +1.0), and described tempo as a closeness-based score rather than a "higher is better" one.
  - Listed the finalized `Song` features (`genre`, `mood`, `tempo_bpm`, `valence`, `danceability`, `acousticness`) and `UserProfile` fields (`favorite_genre`, `favorite_mood`, `target_tempo`, `likes_acoustic`).

---

- Added the missing `target_tempo: float` field to `UserProfile` in `src/recommender.py` so the tempo closeness score has a target value to compare against.
  - Updated both fixtures in `tests/test_recommender.py` to pass `target_tempo=120`.
- Expanded `data/songs.csv` from 10 to 50 songs (40 new entries), adding real, recognizable songs across genres and moods not previously represented in the catalog.
  - New genres: rock (additional), novelty, country (classic and modern), funk, disco, grunge, hip hop, r&b, reggae, edm, metal, punk, folk, classical.
  - New artists include AC/DC, Weird Al Yankovic, Johnny Cash, Dolly Parton, Garth Brooks, Shania Twain, Luke Combs, Morgan Wallen, Kacey Musgraves, Carrie Underwood, Chris Stapleton, Queen, Michael Jackson, Bee Gees, Nirvana, Eminem, Kendrick Lamar, Beyoncé, Whitney Houston, Bob Marley, Daft Punk, Calvin Harris, Metallica, Black Sabbath, The Ramones, Bob Dylan, Simon & Garfunkel, Fleetwood Mac, Adele, Ed Sheeran, Mozart, and Beethoven.
  - Note: `tempo_bpm`, `valence`, `danceability`, and `acousticness` values for these real songs are best-effort estimates for simulation purposes, not pulled from an actual audio-analysis API.

---

- Added `target_valence: float` and `target_danceability: float` to `UserProfile` in `src/recommender.py`, closing the gap where those two `Song` features were collected but had no corresponding target to score against.
  - Updated both fixtures in `tests/test_recommender.py` to pass `target_valence` and `target_danceability`.
- Defined and saved two candidate personas in `src/main.py` for later stress-testing: `INTENSE_ROCK_PROFILE` and `CHILL_LOFI_PROFILE`.
  - Reconciled their dict keys to match the existing functional-API naming convention already used by the starter `user_prefs` example (`genre`, `mood`, `tempo_bpm`, `valence`, `danceability`, `likes_acoustic`) instead of the `UserProfile` dataclass's prefixed field names, so they work with `score_song`/`recommend_songs` without changes to the pre-built functional API.

---

- Finalized the full Algorithm Recipe and documented it, along with an expected-bias note, in `README.md`'s "How The System Works" section: genre match (+2.0), mood match (+1.0), tempo closeness (up to +1.0), valence closeness (up to +0.5), danceability closeness (up to +0.5), and acoustic alignment (+0.5), for a max possible score of 5.5.
- Added `data_flow_diagram.md` to the project root: an ungraded Mermaid flowchart sketching the Phase 2 Step 4 planning aid (Input → per-song scoring loop → sort/rank → top-k output).
