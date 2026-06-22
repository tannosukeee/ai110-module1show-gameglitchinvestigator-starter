from logic_utils import check_guess, parse_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_check_guess_always_returns_a_pair():
    # Targets the bug I fixed: check_guess used to return a bare string on the
    # high/low branches, crashing `outcome, message = check_guess(...)`.
    assert len(check_guess(10, 50)) == 2


def test_parse_guess_valid_integer():
    assert parse_guess("42") == (True, 42, None)


def test_parse_guess_rejects_empty():
    ok, value, error = parse_guess("")
    assert ok is False
    assert value is None


def test_parse_guess_rejects_non_numeric():
    ok, value, error = parse_guess("abc")
    assert ok is False


def test_get_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)