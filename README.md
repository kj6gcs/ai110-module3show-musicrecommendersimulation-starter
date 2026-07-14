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

## How The System Works

**My design:**

Real-world platforms like Spotify blend two approaches: collaborative filtering (what similar users engaged with) and content-based filtering (the attributes of a song itself). This simulation only implements content-based filtering — there's a single simulated user and no interaction history from other users to learn from, so there's nothing for a collaborative approach to work with here.

My version prioritizes **genre** as the strongest signal, since it's the most reliable predictor of whether a listener tolerates a song's overall sound (production style, instrumentation) — a genre mismatch is a harder dealbreaker than a mood mismatch. **Mood** is weighted as a secondary refinement on top of an already-acceptable genre, since mood can vary widely within a single genre or artist (a comedic AC/DC song and an intense AC/DC song are both "rock"). **Tempo** is scored by closeness to the user's preferred pace, rather than simply favoring faster or slower songs — a user who likes 90 BPM songs shouldn't get penalized for a song being slower any more than for it being faster.

- **`Song` features:** `genre`, `mood`, `tempo_bpm`, `valence`, `danceability`, `acousticness`
- **`UserProfile` fields:** `favorite_genre`, `favorite_mood`, `target_tempo`, `target_valence`, `target_danceability`, `likes_acoustic`
- **How songs are chosen:** every song in the catalog is scored against the user profile, then sorted highest-to-lowest and the top `k` are returned

**Algorithm Recipe (finalized):**

| Component              | Points     | Method                                                                                         |
| ---------------------- | ---------- | ---------------------------------------------------------------------------------------------- |
| Genre match            | +2.0       | exact match                                                                                    |
| Mood match             | +1.0       | exact match                                                                                    |
| Tempo closeness        | up to +1.0 | closeness score, scaled by weight, based on distance from `target_tempo`                       |
| Valence closeness      | up to +0.5 | closeness score, scaled by weight, based on distance from `target_valence`                     |
| Danceability closeness | up to +0.5 | closeness score, scaled by weight, based on distance from `target_danceability`                |
| Acoustic alignment     | +0.5       | flat bonus if `likes_acoustic` matches whether the song's `acousticness` is above or below 0.5 |

Max possible score: 5.5.

**Expected bias:** genre and mood together are only worth 3.0 of the 5.5 possible points, while tempo + valence + danceability together can add up to 2.0. That means a song with the _wrong_ genre could still rank competitively on numeric closeness alone if its other attributes line up well with the user's targets — this system may under-penalize genre mismatches more than intended, and it's something to watch for during Phase 4 testing.

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

## Sample Recommendation Output

**Actual output** (`python -m src.main`, Phase 4 stress-test profiles):

**Robby's Profile** — personal taste profile, tested against own intuition

```
User profile: {'genre': 'rock', 'mood': 'intense', 'tempo_bpm': 115, 'valence': 0.55, 'danceability': 0.55, 'likes_acoustic': False}

Top recommendations:

1. Back In Black by AC/DC - Score: 5.38
   Because: genre match (+2.0), mood match (+1.0), tempo closeness (+0.88), valence closeness (+0.50), danceability closeness (+0.50), acoustic alignment (+0.5)

2. Thunderstruck by AC/DC - Score: 5.31
   Because: genre match (+2.0), mood match (+1.0), tempo closeness (+0.89), valence closeness (+0.45), danceability closeness (+0.47), acoustic alignment (+0.5)

3. Storm Runner by Voltline - Score: 5.18
   Because: genre match (+2.0), mood match (+1.0), tempo closeness (+0.77), valence closeness (+0.46), danceability closeness (+0.45), acoustic alignment (+0.5)

4. Dreams by Fleetwood Mac - Score: 4.44
   Because: genre match (+2.0), tempo closeness (+0.97), valence closeness (+0.50), danceability closeness (+0.48), acoustic alignment (+0.5)

5. Big Balls by AC/DC - Score: 4.29
   Because: genre match (+2.0), tempo closeness (+0.92), valence closeness (+0.40), danceability closeness (+0.48), acoustic alignment (+0.5)
```

**Happy Pop**

```
User profile: {'genre': 'pop', 'mood': 'happy', 'tempo_bpm': 120, 'valence': 0.8, 'danceability': 0.8, 'likes_acoustic': False}

Top recommendations:

1. Sunrise City by Neon Echo - Score: 5.46
   Because: genre match (+2.0), mood match (+1.0), tempo closeness (+0.99), valence closeness (+0.48), danceability closeness (+0.49), acoustic alignment (+0.5)

2. I Wanna Dance with Somebody by Whitney Houston - Score: 4.42
   Because: genre match (+2.0), tempo closeness (+0.99), valence closeness (+0.45), danceability closeness (+0.48), acoustic alignment (+0.5)

3. Gym Hero by Max Pulse - Score: 4.37
   Because: genre match (+2.0), tempo closeness (+0.93), valence closeness (+0.48), danceability closeness (+0.46), acoustic alignment (+0.5)

4. Shape of You by Ed Sheeran - Score: 4.30
   Because: genre match (+2.0), tempo closeness (+0.85), valence closeness (+0.48), danceability closeness (+0.48), acoustic alignment (+0.5)

5. Rooftop Lights by Indigo Parade - Score: 3.46
   Because: mood match (+1.0), tempo closeness (+0.97), valence closeness (+0.49), danceability closeness (+0.49), acoustic alignment (+0.5)
```

**Intense Rock**

```
User profile: {'genre': 'rock', 'mood': 'intense', 'tempo_bpm': 140, 'valence': 0.5, 'danceability': 0.55, 'likes_acoustic': False}

Top recommendations:

1. Thunderstruck by AC/DC - Score: 5.41
   Because: genre match (+2.0), mood match (+1.0), tempo closeness (+0.96), valence closeness (+0.47), danceability closeness (+0.47), acoustic alignment (+0.5)

2. Storm Runner by Voltline - Score: 5.36
   Because: genre match (+2.0), mood match (+1.0), tempo closeness (+0.93), valence closeness (+0.49), danceability closeness (+0.45), acoustic alignment (+0.5)

3. Back In Black by AC/DC - Score: 5.20
   Because: genre match (+2.0), mood match (+1.0), tempo closeness (+0.72), valence closeness (+0.47), danceability closeness (+0.50), acoustic alignment (+0.5)

4. Dreams by Fleetwood Mac - Score: 4.33
   Because: genre match (+2.0), tempo closeness (+0.88), valence closeness (+0.47), danceability closeness (+0.48), acoustic alignment (+0.5)

5. Big Balls by AC/DC - Score: 4.28
   Because: genre match (+2.0), tempo closeness (+0.93), valence closeness (+0.38), danceability closeness (+0.48), acoustic alignment (+0.5)
```

**Chill Lofi**

```
User profile: {'genre': 'lofi', 'mood': 'chill', 'tempo_bpm': 75, 'valence': 0.58, 'danceability': 0.6, 'likes_acoustic': True}

Top recommendations:

1. Midnight Coding by LoRoom - Score: 5.46
   Because: genre match (+2.0), mood match (+1.0), tempo closeness (+0.98), valence closeness (+0.49), danceability closeness (+0.49), acoustic alignment (+0.5)

2. Library Rain by Paper Lanterns - Score: 5.46
   Because: genre match (+2.0), mood match (+1.0), tempo closeness (+0.98), valence closeness (+0.49), danceability closeness (+0.49), acoustic alignment (+0.5)

3. Focus Flow by LoRoom - Score: 4.46
   Because: genre match (+2.0), tempo closeness (+0.97), valence closeness (+0.49), danceability closeness (+0.50), acoustic alignment (+0.5)

4. Spacewalk Thoughts by Orbit Bloom - Score: 3.28
   Because: mood match (+1.0), tempo closeness (+0.91), valence closeness (+0.46), danceability closeness (+0.41), acoustic alignment (+0.5)

5. One Love by Bob Marley - Score: 2.37
   Because: tempo closeness (+0.96), valence closeness (+0.44), danceability closeness (+0.48), acoustic alignment (+0.5)
```

**Conflicting (metal + peaceful + fast + acoustic)** — adversarial profile

```
User profile: {'genre': 'metal', 'mood': 'peaceful', 'tempo_bpm': 170, 'valence': 0.85, 'danceability': 0.85, 'likes_acoustic': True}

Top recommendations:

1. Paranoid by Black Sabbath - Score: 3.50
   Because: genre match (+2.0), tempo closeness (+0.95), valence closeness (+0.25), danceability closeness (+0.30)

2. Enter Sandman by Metallica - Score: 3.21
   Because: genre match (+2.0), tempo closeness (+0.71), valence closeness (+0.22), danceability closeness (+0.28)

3. Three Little Birds by Bob Marley - Score: 2.31
   Because: mood match (+1.0), tempo closeness (+0.41), valence closeness (+0.50), danceability closeness (+0.40)

4. Eine kleine Nachtmusik by Mozart - Score: 1.99
   Because: tempo closeness (+0.81), valence closeness (+0.45), danceability closeness (+0.22), acoustic alignment (+0.5)

5. Ring of Fire by Johnny Cash - Score: 1.94
   Because: tempo closeness (+0.69), valence closeness (+0.40), danceability closeness (+0.35), acoustic alignment (+0.5)
```

**No genre+mood match (classical + euphoric)** — adversarial profile

```
User profile: {'genre': 'classical', 'mood': 'euphoric', 'tempo_bpm': 200, 'valence': 0.95, 'danceability': 0.95, 'likes_acoustic': False}

Top recommendations:

1. Eine kleine Nachtmusik by Mozart - Score: 3.20
   Because: genre match (+2.0), tempo closeness (+0.62), valence closeness (+0.40), danceability closeness (+0.18)

2. Don't Stop Me Now by Queen - Score: 3.08
   Because: mood match (+1.0), tempo closeness (+0.72), valence closeness (+0.48), danceability closeness (+0.38), acoustic alignment (+0.5)

3. One More Time by Daft Punk - Score: 2.93
   Because: mood match (+1.0), tempo closeness (+0.52), valence closeness (+0.45), danceability closeness (+0.47), acoustic alignment (+0.5)

4. I Wanna Dance with Somebody by Whitney Houston - Score: 2.92
   Because: mood match (+1.0), tempo closeness (+0.49), valence closeness (+0.48), danceability closeness (+0.45), acoustic alignment (+0.5)

5. Symphony No. 5 by Beethoven - Score: 2.77
   Because: genre match (+2.0), tempo closeness (+0.43), valence closeness (+0.23), danceability closeness (+0.12)
```

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

**Weight shift experiment:** I halved the genre match weight (from +2.0 to +1.0) and doubled the tempo closeness weight (from up to +1.0 to up to +2.0), keeping the overall max possible score the same (5.5), to test how sensitive the rankings were to the chosen weights. The clearest effect showed up in the "No genre+mood match" profile (classical + euphoric): at the original weights, Mozart's genre match alone was enough to rank #1, but under the shifted weights both classical songs (Mozart and Beethoven) fell out of the top 5 entirely, replaced by songs with strong tempo closeness or a mood match instead. A similar effect appeared in the Happy Pop profile, where a mood-only match ("Rooftop Lights") leapfrogged two genre-matched songs into the #2 spot. Profiles where a song already had strong genre, mood, and tempo alignment together (like Intense Rock and my own personal profile) barely changed, since there was nothing for the reweighting to flip. The experiment confirmed the weights are a real, sensitive lever rather than a cosmetic detail — and that the original genre-heavy weighting was a deliberate design choice, since the shifted version produced results that were simply different, not more accurate (a user who explicitly asked for "classical" arguably shouldn't get zero classical songs in their results).

**Feature removal experiment:** I temporarily commented out the mood-match scoring (+1.0) entirely to see how much the rankings would shift without it. The most personally relevant result showed up on my own profile: "Dreams" by Fleetwood Mac jumped to #1, pushing "Back In Black" and "Thunderstruck" down to #2 and #3 — without the mood-match bonus, "Dreams"'s slightly better tempo/valence closeness was enough to win outright, even though I'd already said it isn't a song I'd normally pick. The same thing happened in the Intense Rock profile ("Back In Black" dropped from #3 to #5 once it lost its mood credit), and in the Chill Lofi profile, "Midnight Coding" and "Library Rain" (genre+mood matches) fell into a near-exact tie with "Focus Flow" (genre-only), since mood was the only thing separating them. In the "No genre+mood match" profile, both classical songs (Mozart and Beethoven) took over the top 2 spots uncontested, since nothing else could compete against two genre matches once mood was out of the picture. This change was just different, not more accurate — and for my own profile specifically, it was worse: it demoted the songs I actually like in favor of one I explicitly said isn't my style, which is good evidence that the mood signal, even at a modest +1.0 weight, is doing real personalization work rather than being a redundant afterthought.

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
