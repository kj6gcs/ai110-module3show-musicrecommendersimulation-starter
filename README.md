# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

<!-- Testing to make sure my VS Code is connected back to my GitHub again -->

## How The System Works

**My design:**

Real-world platforms like Spotify blend two approaches: collaborative filtering (what similar users engaged with) and content-based filtering (the attributes of a song itself). This simulation only implements content-based filtering — there's a single simulated user and no interaction history from other users to learn from, so there's nothing for a collaborative approach to work with here.

My version prioritizes **genre** as the strongest signal, since it's the most reliable predictor of whether a listener tolerates a song's overall sound (production style, instrumentation) — a genre mismatch is a harder dealbreaker than a mood mismatch. **Mood** is weighted as a secondary refinement on top of an already-acceptable genre, since mood can vary widely within a single genre or artist (a comedic AC/DC song and an intense AC/DC song are both "rock"). **Tempo** is scored by closeness to the user's preferred pace, rather than simply favoring faster or slower songs — a user who likes 90 BPM songs shouldn't get penalized for a song being slower any more than for it being faster.

- **`Song` features:** `genre`, `mood`, `tempo_bpm`, `valence`, `danceability`, `acousticness`
- **`UserProfile` fields:** `favorite_genre`, `favorite_mood`, `target_tempo`, `target_valence`, `target_danceability`, `likes_acoustic`
- **How songs are chosen:** every song in the catalog is scored against the user profile, then sorted highest-to-lowest and the top `k` are returned

**Algorithm Recipe (finalized):**

| Component | Points | Method |
|---|---|---|
| Genre match | +2.0 | exact match |
| Mood match | +1.0 | exact match |
| Tempo closeness | up to +1.0 | closeness score, scaled by weight, based on distance from `target_tempo` |
| Valence closeness | up to +0.5 | closeness score, scaled by weight, based on distance from `target_valence` |
| Danceability closeness | up to +0.5 | closeness score, scaled by weight, based on distance from `target_danceability` |
| Acoustic alignment | +0.5 | flat bonus if `likes_acoustic` matches whether the song's `acousticness` is above or below 0.5 |

Max possible score: 5.5.

**Expected bias:** genre and mood together are only worth 3.0 of the 5.5 possible points, while tempo + valence + danceability together can add up to 2.0. That means a song with the *wrong* genre could still rank competitively on numeric closeness alone if its other attributes line up well with the user's targets — this system may under-penalize genre mismatches more than intended, and it's something to watch for during Phase 4 testing.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Actual output** (`python -m src.main`, default pop/happy/120 BPM profile):

```
User profile: genre=pop, mood=happy, tempo_bpm=120

Top recommendations:

1. Sunrise City by Neon Echo - Score: 3.99
   Because: genre match (+2.0), mood match (+1.0), tempo closeness (+0.99)

2. I Wanna Dance with Somebody by Whitney Houston - Score: 2.99
   Because: genre match (+2.0), tempo closeness (+0.99)

3. Gym Hero by Max Pulse - Score: 2.92
   Because: genre match (+2.0), tempo closeness (+0.93)

4. Shape of You by Ed Sheeran - Score: 2.85
   Because: genre match (+2.0), tempo closeness (+0.85)

5. Someone Like You by Adele - Score: 2.67
   Because: genre match (+2.0), tempo closeness (+0.67)
```

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
