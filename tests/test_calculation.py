import pytest
from app.calculations import add, subtract

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5), 
    (7, 3, 10),
    (-1, -2, -3)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected

@pytest.mark.parametrize("num1, num2, expected", [
    (5, 1, 4),
    (8, -1, 9),
    (12, 2, 10)
])
def test_subtract(num1, num2, expected):
    assert subtract(num1, num2) == expected
