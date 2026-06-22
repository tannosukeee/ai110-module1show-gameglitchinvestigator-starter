# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

> Note to self: replace every `[CHECK: ...]` marker with what actually happened in your session, then delete the markers before submitting.

## 1. What was broken when you started?

When I first ran the game with `python -m streamlit run app.py`, the app loaded and let me type guesses, but the feedback and the game flow were clearly wrong. The first thing I noticed was that the hints were backwards: when I guessed a number lower than the secret, the game told me my guess was too high instead of too low. The second problem was the attempt counter — the game told me I was out of attempts while I could still see one attempt left, so the round ended one guess too early. The third issue was the "New Game" button: clicking it did nothing, so once a round ended I was stuck and had to rerun the whole app to play again.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| secret 50, guess 40 | "Too Low" hint | "Too High" hint shown | none |
| a wrong guess made while 1 attempt is still left (e.g. attempt 6 of 7) | game keeps going and still lets me guess | "Out of attempts" shown one guess too early | none |
| click "New Game" after the round ended | secret, attempts, and game state reset so I can play again | nothing happens, state does not reset | none |

*(Adjust the exact numbers above to match your real playthrough.)*

---

## 2. How did you use AI as a teammate?

For this project I used Kiro's built-in AI coding assistant — both the agent chat (with `app.py` and `logic_utils.py` attached for context) and the inline chat to ask about specific lines.

**A correct suggestion:** When I described the backwards-hint bug and asked the assistant to explain the logic in `check_guess`, it correctly identified that the comparison was inverted — the branch for `guess < secret` was returning "Too High" instead of "Too Low". I verified this by tracing the function by hand with secret 50 and guess 40, then by running the game again after the fix and confirming that a low guess now returns "Too Low".

**An incorrect or misleading suggestion:** [CHECK: this is a common scenario, but confirm it matches your actual session — if your AI gave a different wrong suggestion, describe that one instead.] When I asked the assistant to fix the "New Game" button, it first suggested only re-generating the secret number inside the button handler. That looked reasonable, but when I tested it the button still seemed dead, because the fix never reset the `game_over` flag (and the attempt counter) in `st.session_state`, so the input stayed locked. I caught this by reviewing the diff and noticing that only `secret` was being reset, then testing the button and seeing the game was still over. I fixed it by resetting all the relevant `session_state` keys and calling `st.rerun()`.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed only when both the live game and an automated test agreed. For the backwards-hint bug, I wrote a pytest test in [CHECK: tests/test_game_logic.py — use whichever test folder name your repo actually has] that asserted `check_guess(50, 60) == "Too High"` and `check_guess(50, 40) == "Too Low"`. Running `pytest`, the test [CHECK: passed — only keep this word if it was actually green when you ran it], which confirmed the comparison was now correct without me having to replay the game every time. I also ran the app with Streamlit and played a full round to confirm the attempt counter stopped at the right time and that the New Game button reset everything. The AI helped by drafting the first version of the test, but I checked that the assertions actually matched the bug — for example, that "Too High" was the exact string the game uses.

---

## 4. What did you learn about Streamlit and state?

I'd explain it like this: every time you interact with a Streamlit app — type something, click a button — Streamlit throws away the running program and runs your whole script again from the top. So a normal variable doesn't survive, because the moment the script reruns it is reset to its starting value. That is why Streamlit gives you `st.session_state`, which works like a small box that stays in place between reruns. Anything you want the app to remember — the secret number, how many attempts are left, whether the game is over — has to live inside that box, not in a normal variable. The New Game bug made this click for me: the fix only worked once I reset the values inside `st.session_state` and told Streamlit to rerun, because that box is the only thing the next rerun actually remembers.

---

## 5. Looking ahead: your developer habits

**A habit I want to reuse:** [CHECK: confirm this is genuinely your takeaway.] The habit I want to keep is writing a small automated test right after fixing a bug instead of only clicking through the app. The pytest test for the high/low logic let me prove the fix in seconds and would catch the bug again if I ever broke it later.

**One thing I'd do differently with AI:** Next time I'll review the diff more carefully before accepting an AI edit, especially for state-related code, because the assistant tends to fix the obvious part and miss the surrounding state that also needs to change.

**How this project changed how I think about AI-generated code:** This project showed me that AI-generated code can look correct and still be subtly broken, so I now treat its output as a draft to verify — by reading the diff and testing it — rather than something to trust on sight.