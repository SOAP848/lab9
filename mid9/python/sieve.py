"""Реализация решета Эратосфена на Python для сравнения с Rust."""

def sieve_of_eratosthenes(n: int) -> list[bool]:
    """Возвращает список is_prime длины n+1, где is_prime[i] = True, если i простое."""
    if n < 2:
        return [False] * (n + 1)
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    limit = int(n ** 0.5) + 1
    for i in range(2, limit):
        if is_prime[i]:
            step = i
            start = i * i
            is_prime[start:n + 1:step] = [False] * ((n - start) // step + 1)
    return is_prime


def primes_upto(n: int) -> list[int]:
    """Возвращает список простых чисел до n (включительно)."""
    is_prime = sieve_of_eratosthenes(n)
    return [i for i in range(2, n + 1) if is_prime[i]]


def count_primes(n: int) -> int:
    """Возвращает количество простых чисел до n."""
    is_prime = sieve_of_eratosthenes(n)
    return sum(1 for i in range(2, n + 1) if is_prime[i])


if __name__ == "__main__":
    # Пример использования
    n = 30
    print(f"Простые числа до {n}: {primes_upto(n)}")
    print(f"Количество простых до {n}: {count_primes(n)}")