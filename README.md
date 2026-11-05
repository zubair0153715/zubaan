# Zubaan — Free AI Language Tutor

Learn English from Urdu — unlimited, free forever. An original,
clean-room answer to the Duolingo Max gap: a top language tier
that costs ~$29.99/month or ~$167.99/year, caps free practice
behind an energy system (2–3 lessons a day even when you answer
everything right), limits its flagship Video Call to ~30-second
exchanges with no pronunciation scoring, and offers no Urdu
course at all.

**Live:** https://clinic-demo.fastapicloud.dev/zubaan

## What it does

1. **Seekho (learn)** — 51 authored words in 3 decks (daily life,
   pharmacy & clinic, university & job), each with Urdu script,
   Roman-Urdu and an example sentence. Tap to flip.
2. **Quiz with explain-every-answer** — 36 grammar items (articles,
   tenses, prepositions, plurals, polite requests). Every answer —
   right or wrong — shows the rule in plain language. The feature
   Duolingo paywalled, then un-paywalled, is the default here.
3. **Guftagu (roleplay)** — 4 full scripted scenarios (shop,
   clinic/pharmacy, university office, job interview) with
   keyword-scored turns, hints and model answers — no 30-second
   limit. Optional AI open chat (Gemini) corrects your sentence
   and continues the scene.
4. **Sunno (dictation)** — listen with your device's own speech
   synthesis, write what you hear; 80% word overlap passes.
   Honest limit, stated on the page: this is dictation-based
   scoring, not acoustic analysis.
5. **Free forever, honest levels** — no account, no card, no energy
   meter. XP, A1→B2 ladder and streak live in your browser
   (localStorage); spaced repetition runs 1/3/7/14/30 days.

## Honest limits

- Starter course, not a 135M-user curriculum: 51 words, 36 quiz
  items, 4 scenarios. New decks are data, not code — the bank is
  designed to grow.
- Builds up to B1/B2 study; no native-fluency claim.
- AI roleplay needs a `GEMINI_API_KEY` in the environment; without
  it, all scripted scenarios, quizzes and dictation still work
  fully, and the page says the AI is off.
- No audio files ship with the app; dictation voice quality
  varies by device.

## Verify

```
~/workspace/.venv-fc/bin/python tests/verify.py
```

## Layout

```
zubaan/            FastAPI package (routes, pages, engine, library, gemini)
tests/verify.py    engine math + bank validity + route smoke tests
```
