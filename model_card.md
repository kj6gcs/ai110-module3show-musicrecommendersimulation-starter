# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

Prompts:

- What kind of recommendations does it generate
- What assumptions does it make about the user
- Is this for real users or classroom exploration

---

## 3. How the Model Works

Explain your scoring approach in simple language.

Prompts:

- What features of each song are used (genre, energy, mood, etc.)
- What user preferences are considered
- How does the model turn those into a score
- What changes did you make from the starter logic

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data

Describe the dataset the model uses.

Prompts:

- How many songs are in the catalog
- What genres or moods are represented
- Did you add or remove data
- Are there parts of musical taste missing in the dataset

---

## 5. Strengths

Where does your system seem to work well

Prompts:

- User types for which it gives reasonable results
- Any patterns you think your scoring captures correctly
- Cases where the recommendations matched your intuition

---

## 6. Limitations and Bias

The catalog is heavily imbalanced by genre: country makes up 22% of the 50 songs (11 tracks), while nine genres — r&b, funk, disco, grunge, jazz, ambient, synthwave, indie pop, and punk — have exactly one song each. Because genre match is worth the most points (+2.0) in the scoring recipe, a user whose favorite genre falls into one of those single-song genres is effectively locked into the same one recommendation every time, no matter how their mood, tempo, or other preferences vary, while a country fan gets 11 different candidates to choose from. This is a real filter bubble, but it comes from the underlying data rather than the scoring logic itself — the recommender can only ever be as diverse as the catalog it's given, and this catalog was hand-curated rather than sampled to represent genres evenly. It's made worse by the fact that mood is an exact string match: even within a genre, a song tagged "aggressive" gets zero credit against a "peaceful" or "intense" preference, so a thin genre with only one mood label offers no flexibility at all.

---

## 7. Evaluation

We tested six profiles: three intuitive "vibe" profiles (Happy Pop, Intense Rock, Chill Lofi), two adversarial profiles built to contain contradictory preferences (a "metal + peaceful + fast + acoustic-loving" profile, and a "classical + euphoric" profile pairing a real genre with a mood that doesn't exist anywhere in that genre in our catalog), and one personal profile built from my own actual stated taste (rock, intense, 115 BPM, moderate valence/danceability, non-acoustic). For each one, we looked at whether the top 5 results matched what the profile was clearly asking for, and whether the point breakdown ("Because: ...") made sense as a plain-language explanation. The biggest surprise was how the adversarial profiles exposed a real weakness: the "peaceful metal" profile still recommended an aggressive Black Sabbath song as its #1 pick, since the genre match (+2.0) alone was enough to outweigh a completely contradicted mood, tempo, and vibe — the system never noticed the preferences didn't make sense together. We also ran a direct side-by-side comparison between the generic Intense Rock profile and my personal profile: lowering the target tempo from 140 to 115 BPM flipped the #1 recommendation from "Thunderstruck" to "Back In Black," driven almost entirely by a tiny valence/danceability match rather than anything resembling "musical taste." On my own profile specifically, "Dreams" by Fleetwood Mac ranked in the top 5 despite having no mood match at all and not being a song I would normally choose — a good example of the system producing a technically defensible but not truly desired recommendation.

**Comparing pairs of profiles, in plain language:**

- **Happy Pop vs. Intense Rock:** these two ask for opposite things (upbeat pop at 120 BPM vs. gritty rock at 140 BPM), and their top-5 lists share zero songs. That makes sense — the genre match alone is usually enough to keep pop and rock from ever mixing, before mood or tempo even get a chance to weigh in.
- **Chill Lofi vs. Intense Rock:** these sit at opposite ends of the tempo range (75 BPM vs. 140 BPM) and opposite moods (chill vs. intense), and again share no songs in their results. This shows tempo closeness is correctly telling "laid-back" apart from "amped-up," not just riding on genre.
- **Intense Rock vs. my own profile:** same genre (rock) and mood (intense), but a different tempo target (140 vs. 115 BPM). This was our cleanest side-by-side test — changing one number (tempo) was enough to flip the #1 song from "Thunderstruck" to "Back In Black," even though every other part of the scoring stayed identical.
- **Conflicting vs. No-genre-mood-match (the two adversarial profiles):** both are designed to confuse the system, but they break it differently. The "Conflicting" profile still has a genre that exists in the catalog (metal), so genre match alone crowns a winner ("Paranoid") even with everything else contradicted. The "No-genre-mood-match" profile pairs a real genre (classical) with a mood no classical song has, so it comes down to a near-tie between a genre match (Mozart) and songs with only a mood match — showing the system gets shakier once genre alone can't settle it.
- **Happy Pop vs. Chill Lofi:** these two are about as far apart as two profiles can be — opposite valence/danceability targets (0.8/0.8 vs. 0.58/0.6), opposite tempo (120 vs. 75 BPM), and opposite acoustic preference (electric vs. acoustic-loving). Their top-5 lists share zero songs, which is exactly what should happen when nearly every dial is turned in the opposite direction.
- **Happy Pop vs. my own profile:** these have genuinely different genre and mood (pop/happy vs. rock/intense), but a nearly identical tempo target (120 vs. 115 BPM). Even with tempo almost matching, their top-5 lists still share zero songs — a good demonstration that genre match is doing the heavy lifting to keep the two lists separate, not tempo.
- **A simple, real example — "Gym Hero" showing up for "Happy Pop":** "Gym Hero" is actually tagged mood "intense," not "happy," so in plain terms: the system saw "this is an upbeat pop song" and let that outweigh the fact that it isn't really a *happy* song. It's not wrong, exactly, but it's a good example of the system settling for "close enough" rather than a true match.

---

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

---

## 9. Personal Reflection

A few sentences about your experience.

Prompts:

- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps
