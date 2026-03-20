import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

from sieve import sieve_of_eratosthenes, primes_upto, count_primes


def test_sieve_basic():
    is_prime = sieve_of_eratosthenes(10)
    assert is_prime[0] is False
    assert is_prime[1] is False
    assert is_prime[2] is True
    assert is_prime[3] is True
    assert is_prime[4] is False
    assert is_prime[5] is True
    assert is_prime[9] is False
    assert is_prime[10] is False


def test_primes_upto():
    assert primes_upto(1) == []
    assert primes_upto(2) == [2]
    assert primes_upto(20) == [2, 3, 5, 7, 11, 13, 17, 19]
    assert primes_upto(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_count_primes():
    assert count_primes(10) == 4
    assert count_primes(30) == 10
    assert count_primes(100) == 25
    assert count_primes(1) == 0
    assert count_primes(2) == 1


def test_sieve_edge_cases():
    # n = 0
    is_prime = sieve_of_eratosthenes(0)
    assert len(is_prime) == 1
    assert is_prime[0] is False
    # n = 1
    is_prime = sieve_of_eratosthenes(1)
    assert len(is_prime) == 2
    assert is_prime[0] is False
    assert is_prime[1] is False
    # n = 2
    is_prime = sieve_of_eratosthenes(2)
    assert is_prime[2] is True


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])