import pytest
from fibonacci.naive import fibonacci_naive
from fibonacci.cached import fibonacci_cached, fibonacci_lru_cached
from fixture import time_tracker
#, (35, 9227465), (40, 102334155)
@pytest.mark.parametrize('n, expected', [(0, 0), (1, 1), (2, 1), (20, 6765), (30, 832040)])
@pytest.mark.parametrize('fib_func', [fibonacci_naive, fibonacci_cached, fibonacci_lru_cached])
def test_fibonacci(time_tracker, fib_func, n, expected):
    res = fib_func(n)
    assert res == expected
