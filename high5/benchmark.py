#!/usr/bin/env python3
"""
Бенчмарк для сравнения производительности трёх реализаций решета Эратосфена:
1. Чистый Python
2. Python + Rust (через ctypes)
3. Python + Go (внешний HTTP сервис)
"""

import time
import subprocess
import sys
import requests
import json
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python'))
from python.sieve import sieve_python

# Попытка загрузить Rust библиотеку через ctypes
RUST_AVAILABLE = False
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'rust'))
    from ctypes_wrapper import sieve_rust
    RUST_AVAILABLE = True
except Exception as e:
    print(f"Rust модуль не найден: {e}. Убедитесь, что библиотека собрана.")

GO_SERVICE_URL = "http://localhost:5000/sieve"
GO_SERVICE_AVAILABLE = False

def check_go_service():
    """Проверяет, запущен ли Go сервис."""
    try:
        resp = requests.get(GO_SERVICE_URL, params={"limit": 10}, timeout=2)
        return resp.status_code == 200
    except:
        return False

def benchmark_python(limit, iterations=10):
    """Замер времени для чистой Python реализации."""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        sieve_python(limit)
        end = time.perf_counter()
        times.append(end - start)
    return times

def benchmark_rust(limit, iterations=10):
    """Замер времени для Rust реализации."""
    if not RUST_AVAILABLE:
        return None
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        sieve_rust(limit)
        end = time.perf_counter()
        times.append(end - start)
    return times

def benchmark_go(limit, iterations=10):
    """Замер времени для Go реализации через HTTP."""
    if not GO_SERVICE_AVAILABLE:
        return None
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        resp = requests.get(GO_SERVICE_URL, params={"limit": limit})
        if resp.status_code != 200:
            print(f"Ошибка Go сервиса: {resp.status_code}")
            return None
        primes = resp.json()
        end = time.perf_counter()
        times.append(end - start)
    return times

def run_benchmarks(limits=[1000, 10000, 50000], iterations=5):
    """Запускает бенчмарки для разных пределов."""
    global GO_SERVICE_AVAILABLE
    GO_SERVICE_AVAILABLE = check_go_service()
    print("=== Бенчмарк решета Эратосфена ===")
    print(f"Python: доступен")
    print(f"Rust: {'доступен' if RUST_AVAILABLE else 'недоступен'}")
    print(f"Go сервис: {'доступен' if GO_SERVICE_AVAILABLE else 'недоступен'}")
    print()

    results = []
    for limit in limits:
        print(f"Лимит = {limit}")
        # Python
        py_times = benchmark_python(limit, iterations)
        py_avg = sum(py_times) / len(py_times) if py_times else 0
        print(f"  Python: среднее {py_avg:.6f} сек, минимум {min(py_times):.6f} сек")

        # Rust
        rust_times = benchmark_rust(limit, iterations)
        if rust_times:
            rust_avg = sum(rust_times) / len(rust_times)
            print(f"  Rust:   среднее {rust_avg:.6f} сек, минимум {min(rust_times):.6f} сек")
            speedup = py_avg / rust_avg if rust_avg > 0 else 0
            print(f"    Ускорение относительно Python: {speedup:.2f}x")
        else:
            rust_avg = None
            print(f"  Rust:   не доступен")

        # Go
        go_times = benchmark_go(limit, iterations)
        if go_times:
            go_avg = sum(go_times) / len(go_times)
            print(f"  Go:     среднее {go_avg:.6f} сек, минимум {min(go_times):.6f} сек")
            speedup = py_avg / go_avg if go_avg > 0 else 0
            print(f"    Ускорение относительно Python: {speedup:.2f}x")
        else:
            go_avg = None
            print(f"  Go:     не доступен")

        results.append({
            "limit": limit,
            "python_avg": py_avg,
            "rust_avg": rust_avg,
            "go_avg": go_avg,
        })
        print()
    return results

def build_rust():
    """Собирает Rust библиотеку."""
    print("Сборка Rust модуля...")
    result = subprocess.run(
        ["cargo", "build", "--release"],
        cwd=os.path.join(os.path.dirname(__file__), "rust"),
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Ошибка сборки Rust: {result.stderr}")
        return False
    print("Rust модуль собран.")
    return True

def start_go_service():
    """Запускает Go сервис в фоновом процессе."""
    print("Запуск Go сервиса...")
    go_dir = os.path.join(os.path.dirname(__file__), "go")
    exe_path = os.path.join(go_dir, "sieve_go.exe")
    if not os.path.exists(exe_path):
        print("Go исполняемый файл не найден, компилируем...")
        result = subprocess.run(
            ["go", "build", "-o", "sieve_go.exe", "main.go"],
            cwd=go_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Ошибка сборки Go: {result.stderr}")
            return
    # Запуск сервиса
    try:
        subprocess.Popen(
            [exe_path],
            cwd=go_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(2)  # Даём время на запуск
        print("Go сервис запущен.")
    except Exception as e:
        print(f"Не удалось запустить Go сервис: {e}")

def main():
    global RUST_AVAILABLE, GO_SERVICE_AVAILABLE
    # Сборка Rust
    if not RUST_AVAILABLE:
        build_rust()
        # Попробуем загрузить снова
        try:
            from ctypes_wrapper import sieve_rust
            RUST_AVAILABLE = True
        except ImportError:
            print("Не удалось загрузить Rust модуль после сборки.")

    # Запуск Go сервиса
    if not check_go_service():
        start_go_service()
        # Проверяем ещё раз
        GO_SERVICE_AVAILABLE = check_go_service()

    # Запуск бенчмарков
    results = run_benchmarks()

    # Вывод сводки
    print("\n=== Сводка ===")
    for r in results:
        print(f"Лимит {r['limit']}: Python {r['python_avg']:.6f} сек, "
              f"Rust {r['rust_avg'] if r['rust_avg'] else 'N/A'}, "
              f"Go {r['go_avg'] if r['go_avg'] else 'N/A'}")

if __name__ == "__main__":
    main()