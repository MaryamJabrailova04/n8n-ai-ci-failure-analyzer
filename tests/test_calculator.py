from app.calculator import add


def test_add_returns_correct_sum() -> None:
    assert add(2, 3) == 9
