from logic_utils import check_guess, update_score


# ── Existing tests (fixed: check_guess returns a tuple, not a plain string) ──

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ── Bug 1: hint direction was backwards ──
# Before fix: guess > secret returned "Go HIGHER!" (wrong)
# After fix:  guess > secret returns "Go LOWER!"

def test_too_high_hint_says_go_lower():
    # Guess is 60, secret is 50 → guess is too high → player must go lower
    _, message = check_guess(60, 50)
    assert "LOWER" in message, f"Expected 'LOWER' in hint, got: {message}"

def test_too_low_hint_says_go_higher():
    # Guess is 40, secret is 50 → guess is too low → player must go higher
    _, message = check_guess(40, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint, got: {message}"


# ── Bug 2: wrong guess on even attempts gave +5 score ──
# Before fix: update_score(..., "Too High", attempt_number=2) returned current + 5
# After fix:  always returns current - 5

def test_too_high_on_even_attempt_deducts_score():
    # attempt_number=2 (even) used to reward +5 — now must deduct 5
    result = update_score(100, "Too High", attempt_number=2)
    assert result == 95, f"Expected 95, got {result}"

def test_too_high_on_odd_attempt_deducts_score():
    result = update_score(100, "Too High", attempt_number=3)
    assert result == 95, f"Expected 95, got {result}"

def test_too_low_always_deducts_score():
    result = update_score(100, "Too Low", attempt_number=2)
    assert result == 95, f"Expected 95, got {result}"


# ── Bug 5: secret type flip (int vs str comparison) ──
# Before fix: on even attempts, secret was cast to str so check_guess(50, "50")
# would fall into TypeError path and use string comparison ("9" > "10" is True).
# After fix:  always integers, so numeric comparison is correct.

def test_check_guess_integer_comparison_not_string():
    # "9" > "10" is True in Python string comparison → would wrongly say Too High
    # With integer comparison 9 < 10 → correctly says Too Low
    outcome, message = check_guess(9, 10)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_check_guess_win_with_integers():
    outcome, _ = check_guess(42, 42)
    assert outcome == "Win"
