# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game purpose:** A number guessing game built with Streamlit. The app picks a secret number between 1 and 100, and the player tries to guess it within a limited number of attempts, receiving a "Too High" or "Too Low" hint after each guess.
- [x] **Bugs found:**
  - Unwinnable game — guessing the exact secret never triggered a win, so the round never ended.
  - Blank hints — the hint area stayed empty after every guess, even with "Show hint" checked.
  - Frozen score — the score stayed at 0 regardless of the guesses made.
  - Root cause for all three: `app.py` did `outcome = check_guess(...)`, but `check_guess` returns a `(outcome, message)` tuple, so the win check, hint lookup, and score update all received a tuple instead of a string.
  - Shadowed imports — `app.py` re-defined `get_range_for_difficulty`, `parse_guess`, and `update_score` after importing them from `logic_utils.py`; the local `update_score` was a buggy version that changed the score based on odd/even attempt numbers.
- [x] **Fixes applied:**
  - Unpacked the `(outcome, message)` pair returned by `check_guess`, so the game can be won, hints display correctly, and the score updates.
  - Removed the duplicate function definitions in `app.py` that shadowed the imports from `logic_utils.py`, so the app uses the single, tested logic in `logic_utils.py`.
  - Cleaned up dead code in `app.py` (an unused `secret = str(...)` line and a duplicated `st.warning(message)` call).

## 📸 Demo Walkthrough

1. The app starts and picks a secret number between 1 and 100, showing the player how many attempts they have.
2. The player enters a guess of 40 and clicks Submit; the secret is higher, so the game shows the "Go higher." hint.
3. The player enters a guess of 70; the secret is lower, so the game shows the "Go lower." hint.
4. After each guess the attempts-left counter decreases by one, and the secret number stays the same throughout the round.
5. The player guesses the secret number correctly; the game shows a win message with the final score and stops accepting new guesses.
6. The player clicks "New Game"; the secret, attempts, score, and game state reset, and a fresh round begins.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results
```
============================= test session starts =============================
platform win32 -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0
rootdir: ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.14.0, asyncio-1.4.0
collected 8 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 12%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 25%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 37%]
tests/test_game_logic.py::test_check_guess_always_returns_a_pair PASSED  [ 50%]
tests/test_game_logic.py::test_parse_guess_valid_integer PASSED          [ 62%]
tests/test_game_logic.py::test_parse_guess_rejects_empty PASSED          [ 75%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric PASSED    [ 87%]
tests/test_game_logic.py::test_get_range_normal PASSED                   [100%]

============================== 8 passed in 0.05s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]