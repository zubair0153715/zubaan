"""Zubaan verification — engine math, content bank, routes.

Run: ~/workspace/.venv-fc/bin/python tests/verify.py
Exit code 0 = all pass. No network, no key needed (AI tests only
check the no-key error path, never a live call).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from zubaan import engine, library  # noqa: E402

PASS = 0
FAIL = []


def check(name, cond, extra=""):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(f"{name} {extra}")


# --- levels / XP ---
check("level A1 at 0", engine.level_for(0) == "A1")
check("level A2 at 200", engine.level_for(200) == "A2")
check("level A2 at 599", engine.level_for(599) == "A2")
check("level B1 at 600", engine.level_for(600) == "B1")
check("level B2 at 1200", engine.level_for(1200) == "B2")
check("level B2 beyond", engine.level_for(99999) == "B2")
xp, lvl, changed = engine.award_xp(195, 10)
check("award crosses level", (xp, lvl, changed) == (205, "A2", True))
xp, lvl, changed = engine.award_xp(100, 10)
check("award no cross", (xp, lvl, changed) == (110, "A1", False))
check("award never negative", engine.award_xp(5, -20)[0] == 0)

# --- SRS ---
check("srs box0 +1d", engine.srs_next(0, "2026-11-05") == "2026-11-06")
check("srs box1 +3d", engine.srs_next(1, "2026-11-05") == "2026-11-08")
check("srs box2 +7d", engine.srs_next(2, "2026-11-05") == "2026-11-12")
check("srs box3 +14d", engine.srs_next(3, "2026-11-05") == "2026-11-19")
check("srs box4 +30d", engine.srs_next(4, "2026-11-05") == "2026-12-05")
check("srs box clamped", engine.srs_next(9, "2026-11-05") == "2026-12-05")

# --- roleplay scoring ---
m, t, p = engine.score_roleplay_step(
    ["assalam", "notebook", "need"], "Walaikum Assalam! I need a notebook.")
check("roleplay full match", (m, t, p) == (3, 3, True))
m, t, p = engine.score_roleplay_step(
    ["assalam", "notebook", "need", "discount"], "I need a notebook.")
check("roleplay half passes", (m, t, p) == (2, 4, True))
m, t, p = engine.score_roleplay_step(
    ["assalam", "notebook", "need", "discount"], "Hello there.")
check("roleplay zero fails", (m, t, p) == (0, 4, False))
m, t, p = engine.score_roleplay_step(
    ["how many"], "How many times a day?")
check("roleplay phrase keyword", (m, t, p) == (1, 1, True))
m, t, p = engine.score_roleplay_step(
    ["how many"], "How much is it?")
check("roleplay phrase no partial", (m, t, p) == (0, 1, False))

# --- dictation ---
f, p = engine.dictation_score("Take this medicine after meals.",
                              "take this medicine after meals")
check("dictation exact", (f, p) == (1.0, True))
f, p = engine.dictation_score("Take this medicine after meals.",
                              "take medicine after")
check("dictation 3/5 fails", abs(f - 0.6) < 1e-9 and p is False)
f, p = engine.dictation_score("Take this medicine after meals.",
                              "take this medicine after school")
check("dictation 4/5 passes", abs(f - 0.8) < 1e-9 and p is True)
f, p = engine.dictation_score("Take this medicine after meals.", "")
check("dictation empty fails", (f, p) == (0.0, False))

# --- quiz ---
item = library.GRAMMAR[0]["items"][0]
check("quiz right", engine.check_quiz(item, 1) is True)
check("quiz wrong", engine.check_quiz(item, 0) is False)
check("quiz bad index", engine.check_quiz(item, 9) is False)

# --- bank ---
errs = engine.validate_bank(library)
check("bank valid", errs == [], str(errs))
n_vocab = sum(len(d["words"]) for d in library.VOCAB)
check("vocab count 51", n_vocab == 51, str(n_vocab))
n_grammar = sum(len(t["items"]) for t in library.GRAMMAR)
check("grammar count 36", n_grammar == 36, str(n_grammar))
check("scenario count 4", len(library.SCENARIOS) == 4)
check("every scenario 4 steps",
      all(len(s["steps"]) == 4 for s in library.SCENARIOS))

# --- routes via TestClient ---
try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from zubaan.routes import router

    app = FastAPI()
    app.include_router(router)
    c = TestClient(app)
    r = c.get("/zubaan")
    check("route page 200", r.status_code == 200 and "Zubaan" in r.text)
    r = c.get("/zubaan/api/bank")
    check("route bank valid", r.status_code == 200 and r.json()["valid"] is True)
    r = c.get("/zubaan/api/ai-status")
    check("route ai-status", r.status_code == 200
          and r.json()["ai_available"] is False)
    r = c.post("/zubaan/api/score-step",
               data={"payload": '{"keywords": ["fever"], "text": "I have a fever"}'})
    check("route score-step", r.status_code == 200 and r.json()["passed"] is True)
    r = c.post("/zubaan/api/dictation",
               data={"payload": '{"target": "Take this medicine after meals.", "typed": "take this medicine after meals"}'})
    check("route dictation", r.status_code == 200 and r.json()["passed"] is True)
    r = c.post("/zubaan/api/roleplay", data={"text": "Hello"})
    check("route roleplay no-key error", r.status_code == 200
          and r.json()["ok"] is False)
except ImportError as e:
    FAIL.append(f"testclient import failed: {e}")

print(f"{PASS} PASS, {len(FAIL)} FAIL")
for f in FAIL:
    print("FAIL:", f)
sys.exit(1 if FAIL else 0)
