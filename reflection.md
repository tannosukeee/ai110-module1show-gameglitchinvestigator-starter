# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game with `python -m streamlit run app.py`, the app loaded and let me type guesses, but the feedback and the scoring were clearly broken. The first thing I noticed was that I could never win: even when I guessed the exact secret number shown in the Developer Debug Info, the game kept accepting guesses instead of declaring a win. The second problem was the hints — after every guess the hint area stayed blank, so the game never told me whether to go higher or lower even with "Show hint" checked. The third issue was the score: it stayed frozen at 0 no matter how many guesses I made, and even when I traced the logic it seemed to follow a strange odd/even rule that didn't match the clean `update_score` in `logic_utils.py`.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| secret 50, guess 50 | "Correct!" / win message, game ends | game keeps accepting guesses, never wins | none |
| secret 50, guess 40 (Show hint on) | "Go higher." hint shown | hint area is blank | none |
| any wrong guess | score changes (e.g. -5) | score stays at 0 | none |

*(Adjust the exact numbers above to match your real playthrough.)*

---

## 2. How did you use AI as a teammate?

For this project I used Kiro's built-in AI coding assistant — both the agent chat (with `app.py` and `logic_utils.py` attached for context) and the inline chat to ask about specific lines.

**A correct suggestion:** When I described the unwinnable-game bug and asked the assistant to explain why `outcome == "Win"` never matched, it correctly spotted that `check_guess` returns a `(outcome, message)` tuple but the code did `outcome = check_guess(...)`, so `outcome` was the whole tuple. That single bug explained all three symptoms at once: the win check failed, `hint_messages.get(tuple)` returned a blank string, and the score never updated. I verified this by printing the return value, then unpacking it as `outcome, message = check_guess(...)` and confirming in the live game that I could finally win, see hints, and watch the score change.

**An incorrect or misleading suggestion:** When I asked the assistant to fix the frozen score, it first suggested editing the `update_score` function defined inside `app.py` to remove the odd/even logic. That looked reasonable, but it was misleading: `app.py` already imports `update_score` from `logic_utils.py` at the top, and that local definition was a duplicate shadowing the import. Patching the duplicate would have left two competing versions of the same function. I caught this by reviewing the diff and noticing the import line, then deleted the duplicate definitions in `app.py` entirely so the app uses the single, tested version in `logic_utils.py`.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed only when both the live game and an automated test agreed. For the tuple-unpacking bug, the key test in `tests/test_game_logic.py` was `test_check_guess_always_returns_a_pair`, which asserts `len(check_guess(10, 50)) == 2`, plus tests like `test_guess_too_high` and `test_guess_too_low` that unpack `outcome, message = check_guess(...)` exactly the way the app now does. Running `pytest`, all of them passed (`8 passed in 0.05s`), which confirmed `check_guess` returns a usable pair without me having to replay the game every time. I also ran the app with Streamlit and played a full round to confirm I could actually win, that hints appeared, and that the score moved off 0. The AI helped by drafting the first version of the tests, but I checked that the assertions matched the real outcome strings — for example, that "Too High" and "Win" were the exact values the game compares against.

---

## 4. What did you learn about Streamlit and state?

I'd explain it like this: every time you interact with a Streamlit app — type something, click a button — Streamlit throws away the running program and runs your whole script again from the top. So a normal variable doesn't survive, because the moment the script reruns it is reset to its starting value. That is why Streamlit gives you `st.session_state`, which works like a small box that stays in place between reruns. Anything you want the app to remember — the secret number, how many attempts are left, whether the game is over — has to live inside that box, not in a normal variable. Studying this game made it click: the secret is generated with `if "secret" not in st.session_state` precisely so it isn't re-rolled on every rerun, and the "New Game" button only works because it overwrites those `session_state` keys and then calls `st.rerun()` so the next run reads the fresh values.

---

## 5. Looking ahead: your developer habits

**A habit I want to reuse:** The habit I want to keep is writing a small automated test right after fixing a bug instead of only clicking through the app. The `test_check_guess_always_returns_a_pair` test let me prove the fix in seconds and would catch the bug again if someone ever changed `check_guess` back to returning a bare string.

**One thing I'd do differently with AI:** Next time I'll review the diff more carefully before accepting an AI edit, especially when there are duplicate function definitions, because the assistant tends to patch the copy it sees first instead of noticing that an import is being shadowed.

**How this project changed how I think about AI-generated code:** This project showed me that AI-generated code can look correct and still be subtly broken, so I now treat its output as a draft to verify — by reading the diff and testing it — rather than something to trust on sight.