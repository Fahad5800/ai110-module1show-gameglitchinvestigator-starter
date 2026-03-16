# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

---
- The Attempts count down is broken. In the screen where we guess number, number of attempts is different compared to settings and Developer bug info. Also, the attempts count down is not consistent.

- The range is not strict - meaning we are able to put negative integers.

- The range difficulty is broken, hard should be more then easy and normal\

- Each difficulty selection should prompt the user about the specific range

- Hints are inconsistent
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---
- I used Claude AI to solve the range difficulty problem.
- I asked question whether my concern regarding it is valid and it answered yes. I verfied it by checking the code because in code the easy and normal had range 1-20 and 1-100 respectively while hard had a range 1-50 which was off.
- However, it misleaded me by telling me to increase the range to 1-200. I know this is not correct because the game is designed to guess number between 1 to 100.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

I decided a bug was really fixed when I could trace the correct logic by reading the code AND confirm the expected output with a passing pytest test. Reading alone was not enough because the secret type-flip bug looked subtle in code, so having a test that failed before the fix and passed after gave me confidence the repair was real.

**pytest test I ran — `test_too_high_hint_says_go_lower`:**
This test called `check_guess(60, 50)` and asserted that the returned message contained "LOWER". Before the fix the original code returned "Go HIGHER!" for that input, so the test would have failed. After swapping the messages in `logic_utils.py`, the test passed. This showed me that the hint direction bug was fully fixed and not just visually different.

**pytest test I ran — `test_too_high_on_even_attempt_deducts_score`:**
This test called `update_score(100, "Too High", attempt_number=2)` and asserted the result was 95. Before the fix, even attempts returned `current_score + 5` (105), so this test would have failed. After removing the even/odd branch it returned 95 and the test passed, confirming the scoring bug was resolved.

**How AI helped design the tests:**
Claude AI wrote all the pytest cases in 'tests/test_game_logic.py'. It also spotted that the existing three tests were broken — they compared 'check_guess(...)' against a plain string like "Win", but the function actually returns a tuple '(outcome, message)'. Claude fixed those tests and added new ones that directly targeted each bug, which helped me understand what "testing the fix" actually means versus just testing the happy path.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

The secret number kept changing because the original code called 'random.ranint()' at the top of the script with no condition. Every time I clicked "Submit Guess", Streamlit re-ran the entire script from the top, which picked a brand new random number each time. So I was always chasing a moving target.

Streamlit works like a refresh button that never stops — every interaction (a click, a text input, a checkbox) causes the whole Python file to run again from line 1. Session state is like a small notebook that Streamlit saves between those reruns. Anything you store in `st.session_state' survives the rerun, while regular variables just get reset.

The fix was wrapping the random number generation in an 'if "secret" not in st.session_state:` check (app.py line 32–33). This means the secret is only generated once — the very first time the app loads — and every rerun after that just reads the existing value from session state instead of creating a new one.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

---

One thing I learned from all this experience is the importance of correct documentation and pytest. I learned that before jumping into fixing things, I should first familiarize myself with the project, then start developing correct pytest be observing and documenting the behaviour of the app. After this, we can correctly validate and work on fixing the errors. 
This projects helped me to use AI-tools more proficiently. Now I know that not every suggesiton from AI is correct and we need human judgement to validate the authenticity of AI-generated code. Overall, this was a fun experience and I was able to better understand the documentation and use of github more clearly. 

