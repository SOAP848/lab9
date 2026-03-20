#!/usr/bin/env python3
"""
Бенчмарк сравнения скорости выполнения решета Эратосфена на Rust и Python.
"""

import subprocess
import sys
import time
import statistics
from pathlib import Path

# Добавляем путь к модулю Python
sys.path.insert(0, str(Path(__file__).parent / "python"))
try:
    from sieve import sieve_of_eratosthenes as py_sieve
except ImportError as e:
    print(f"Ошибка импорта Python модуля: {e}")
    sys.exit(1)


def run_rust_via_cli(n: int, iterations: int = 10) -> float:
    """Запускает Rust реализацию через CLI и возвращает среднее время в секундах."""
    rust_dir = Path(__file__).parent / "rust"
    cargo_toml = rust_dir / "Cargo.toml"
    if not cargo_toml.exists():
        print("Ошибка: Cargo.toml не найден")
        return 0.0

    # Компилируем в release режиме (если ещё не скомпилировано)
    build_result = subprocess.run(
        ["cargo", "build", "--release"],
        cwd=rust_dir,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore',
    )
    if build_result.returncode != 0:
        print("Ошибка сборки Rust:")
        print(build_result.stderr)
        return 0.0

    # Запускаем бинарник с аргументами
    bin_path = rust_dir / "target" / "release" / "sieve_bench.exe"
    if not bin_path.exists():
        # На Linux расширение .exe отсутствует
        bin_path = rust_dir / "target" / "release" / "sieve_bench"
    if not bin_path.exists():
        print(f"Бинарник не найден: {bin_path}")
        return 0.0

    # Замеряем время выполнения одной итерации через subprocess
    # Rust программа сама делает iterations итераций и выводит среднее.
    # Мы можем просто запустить её и распарсить вывод.
    try:
        result = subprocess.run(
            [str(bin_path), str(n), str(iterations)],
            cwd=rust_dir,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
        )
    except Exception as e:
        print(f"Ошибка запуска Rust бенчмарка: {e}")
        return 0.0

    if result.returncode != 0:
        print("Ошибка выполнения Rust бенчмарка:")
        print(result.stderr)
        return 0.0

    if result.stdout is None:
        print("Нет вывода от Rust бенчмарка")
        return 0.0

    # Парсим вывод, ищем строку "Среднее время: X.XXXXXX сек"
    for line in result.stdout.splitlines():
        if "Среднее время:" in line:
            parts = line.split()
            # Ищем число
            for part in parts:
                try:
                    return float(part)
                except ValueError:
                    continue
    print("Не удалось извлечь среднее время из вывода Rust")
    return 0.0


def benchmark_python(n: int, iterations: int = 10) -> float:
    """Замер времени выполнения Python реализации."""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        py_sieve(n)
        end = time.perf_counter()
        times.append(end - start)
    return statistics.mean(times)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Сравнение Rust и Python")
    parser.add_argument("-n", type=int, default=1_000_000,
                        help="Верхняя граница решета")
    parser.add_argument("--iterations", type=int, default=10,
                        help="Количество итераций для усреднения")
    args = parser.parse_args()

    print(f"Бенчмарк решета Эратосфена до n = {args.n}")
    print(f"Итераций: {args.iterations}")
    print()

    # Python
    print("Запуск Python...")
    py_time = benchmark_python(args.n, args.iterations)
    print(f"Python среднее время: {py_time:.6f} сек")

    # Rust
    print("Запуск Rust...")
    rust_time = run_rust_via_cli(args.n, args.iterations)
    if rust_time > 0:
        print(f"Rust среднее время: {rust_time:.6f} сек")
        speedup = py_time / rust_time if rust_time != 0 else float('inf')
        print(f"Ускорение Rust относительно Python: {speedup:.2f}x")
    else:
        print("Rust бенчмарк недоступен")

    # Дополнительно: можно сравнить с оптимизированной версией Python (numpy)
    # но это не требуется.


if __name__ == "__main__":
    main()