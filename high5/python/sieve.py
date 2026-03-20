"""
Реализация решета Эратосфена на чистом Python.
"""

def sieve_python(limit: int) -> list[int]:
    """
    Возвращает список простых чисел до limit (включительно).

    Args:
        limit: верхняя граница поиска простых чисел.

    Returns:
        Список простых чисел.
    """
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            step = i
            start = i * i
            sieve[start:limit + 1:step] = [False] * ((limit - start) // step + 1)
    return [i for i, is_prime in enumerate(sieve) if is_prime]


if __name__ == "__main__":
    # Пример использования
    primes = sieve_python(100)
    print(f"Простые числа до 100: {primes}")
    print(f"Количество: {len(primes)}")