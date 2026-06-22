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
  - Inverted hints — a guess lower than the secret was reported as "Too High" instead of "Too Low".
  - Off-by-one attempt counter — the game reported being out of attempts while one valid attempt was still left, ending the round one guess too early.
  - Broken "New Game" button — clicking it did nothing because the game state in `st.session_state` was never reset.
  - [CHECK: The mission above references a secret-number-resetting state bug. Open the "Developer Debug Info" tab, click Submit a few times, and confirm whether the secret changes on every submit. If it does, document it here as a bug and remove this note; if it does not, delete this line.]
- [x] **Fixes applied:**
  - Corrected the comparison in `check_guess` so a low guess returns "Too Low" and a high guess returns "Too High".
  - Fixed the end-of-game condition so the round only ends when no attempts remain.
  - Reset all relevant `st.session_state` keys (secret, attempts, and the game-over flag) inside the "New Game" handler and called `st.rerun()`.
  - Refactored the core logic (`check_guess`, `parse_guess`) out of `app.py` into `logic_utils.py`.

## 📸 Demo Walkthrough

1. The app starts and picks a secret number between 1 and 100, showing the player how many attempts they have.
2. The player enters a guess of 40 and clicks Submit; the game returns "Too Low".
3. The player enters a guess of 70; the game returns "Too High".
4. After each guess the attempt counter decreases by one, and the secret number stays the same throughout the round.
5. The player guesses the secret number correctly; the game shows a win message and stops accepting new guesses.
6. The player clicks "New Game"; the secret, attempts, and game state reset, and a fresh round begins.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

<!-- CHECK: run pytest and paste your real terminal output below. Do not leave the placeholder text. -->

```
$ pytest
# Paste your actual output here, e.g.:
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]