import pytest
from fibonacci.naive import fibonacci_naive
from fibonacci.cached import fibonacci_cached, fibonacci_lru_cached

@pytest.mark.parametrize('fib_func', [fibonacci_naive, fibonacci_cached, fibonacci_lru_cached])
@pytest.mark.parametrize('n, expected', [(0, 0), (1, 1), (2, 1), (20, 6765)])
def test_fibonacci(fib_func, n, expected):
    res = fib_func(n)
    assert res == expected
