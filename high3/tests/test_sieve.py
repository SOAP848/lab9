import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

from sieve import sieve_primes, count_primes

def test_primes_up_to_10():
    primes = sieve_primes(10)
    assert primes == [2, 3, 5, 7]

def test_primes_up_to_0():
    primes = sieve_primes(0)
    assert primes == []

def test_primes_up_to_1():
    primes = sieve_primes(1)
    assert primes == []

def test_primes_up_to_2():
    primes = sieve_primes(2)
    assert primes == [2]

def test_primes_up_to_30():
    primes = sieve_primes(30)
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert primes == expected

def test_count_primes():
    assert count_primes(10) == 4
    assert count_primes(0) == 0
    assert count_primes(1) == 0
    assert count_primes(2) == 1
    assert count_primes(30) == 10

def test_negative_limit():
    try:
        sieve_primes(-5)
        assert False, "Expected ValueError"
    except ValueError:
        pass
    try:
        count_primes(-5)
        assert False, "Expected ValueError"
    except ValueError:
        pass

def test_large_limit():
    # Just ensure no crash
    primes = sieve_primes(100)
    assert len(primes) == 25
    assert primes[0] == 2
    assert primes[-1] == 97

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])