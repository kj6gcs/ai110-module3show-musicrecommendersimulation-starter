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

---

- **Bug fix (discovered by Claude):** `src/main.py` imported `from recommender import ...`, which fails with `ModuleNotFoundError` under the documented `python -m src.main` run command (no top-level `recommender` module exists; it lives at `src/recommender.py`). Changed to `from src.recommender import ...`, matching the import style already used in `tests/test_recommender.py`.
- Implemented `load_songs()` in `src/recommender.py` using `csv.DictReader`, converting `id` to `int` and `tempo_bpm`/`valence`/`danceability`/`acousticness` to `float` so they're ready for scoring math. Verified via `python -m src.main`, which now prints `Loaded songs: 50`.

---

- Implemented `score_song()` in `src/recommender.py` using the finalized Algorithm Recipe (genre match +2.0, mood match +1.0, tempo/valence/danceability closeness up to +1.0/+0.5/+0.5, acoustic alignment +0.5), returning both a numeric score and a list of human-readable reasons.
  - Added two helper functions: `normalize_tempo()` (scales `tempo_bpm` to 0-1) and `closeness_score()` (rewards values close to a target rather than simply higher/lower ones).
  - Uses `.get()`/`in` checks on `user_prefs` so partial profiles (like the 3-key starter `user_prefs`) score correctly without requiring every field.
  - Verified with a quick ad hoc script scoring the first 3 songs against the starter profile — results matched the expected recipe behavior.

---

- Implemented `recommend_songs()` in `src/recommender.py`: scores every song in the catalog via `score_song()`, ranks with `sorted()` (chosen over `.sort()` since it returns a new list rather than mutating in place), and returns the top `k` as `(song, score, explanation)` tuples with reasons joined into a readable string.
  - Verified via `python -m src.main`: the starter pop/happy/120 BPM profile correctly returns "Sunrise City" as the top recommendation (full genre + mood match, near-perfect tempo closeness).

---

- Cleaned up the CLI output formatting in `src/main.py`: numbered each recommendation, added the artist name, and echoed the active user profile above the results list.
  - Swapped an em dash for a plain hyphen after the Windows terminal mis-rendered it as `�` under the console's active encoding.
  - Pasted the verified `python -m src.main` output into `README.md`'s "Sample Recommendation Output" section as a fenced code block.

---

- Condensed the docstrings on `load_songs()`, `score_song()`, and `recommend_songs()` in `src/recommender.py` to single lines, per the Phase 3 documentation step.
  - Re-verified with `python -m src.main` and `pytest` (2 passed) after the cleanup — no behavior changes.

---

- Added Phase 4 Step 1 stress-test profiles to `src/main.py`: formalized the starter profile as `HAPPY_POP_PROFILE`, and added two adversarial profiles (`CONFLICTING_PROFILE` and `NO_GENRE_MOOD_MATCH_PROFILE`) designed to probe internally contradictory or unmatchable preferences.
  - Updated `main()` to loop over all five profiles via a `STRESS_TEST_PROFILES` dict and print labeled recommendations for each.
  - Ran the CLI and pasted the real output for all five profiles into `README.md`'s "Sample Recommendation Output" section as separate fenced code blocks, replacing the old placeholder text.
  - Notable finding: the "Conflicting" profile (metal + peaceful + fast + acoustic-loving) still recommended an aggressive Black Sabbath song as #1, since the genre match (+2.0) outweighed the mismatched mood/valence — a concrete example of the bias already predicted in the README.

---

- Added `ROBBYS_PROFILE` to `src/main.py`'s `STRESS_TEST_PROFILES`: a personal taste profile (rock, intense, 115 BPM, valence/danceability 0.55, non-acoustic) built from the developer's own stated preferences, used to sanity-check the recommender against real musical intuition rather than a synthetic persona.
  - Ran it against the recommender and pasted the output at the top of `README.md`'s "Sample Recommendation Output" section, ahead of the five stress-test profiles.
  - Notable finding: compared to the generic "Intense Rock" profile, lowering the target tempo from 140 to 115 BPM flipped the #1 result from "Thunderstruck" to "Back In Black" — driven by a near-exact valence/danceability match rather than tempo. "Dreams" by Fleetwood Mac also placed in the top 5 with no mood match, which the developer confirmed isn't a song they'd normally pick, despite it being a defensible score-wise recommendation.
- Added a paragraph to `model_card.md`'s Section 7 (Evaluation) summarizing which profiles were tested, what was looked for, what surprised us (the adversarial-profile bias and the personal-profile tempo-flip/"Dreams" finding), and the direct Intense-Rock-vs-personal-profile comparison.

---

- Ran two Phase 4 Step 3 sensitivity experiments in `src/recommender.py`, each applied temporarily and reverted afterward (confirmed via `python -m src.main` and `pytest`, 2 passed):
  - **Weight shift:** halved genre match (+2.0 → +1.0) and doubled tempo closeness (up to +1.0 → up to +2.0). Both classical songs fell out of the "No genre+mood match" profile's top 5 entirely, and a mood-only match leapfrogged two genre matches in the Happy Pop profile.
  - **Feature removal:** commented out the mood-match scoring entirely. On my own profile, "Dreams" by Fleetwood Mac jumped to #1 over "Back In Black" and "Thunderstruck" — demoting songs I actually like in favor of one I'd already said isn't my style.
  - Documented both experiments in first person in `README.md`'s "Experiments You Tried" section.
