# Лабораторная работа №9 — Вариант 9

## mid4: Python <-> Go через JSON (stdin/stdout)

Проект демонстрирует обмен данными между Python и Go по контракту JSON:

- Python отправляет запрос в Go через `stdin`
- Go читает JSON из `stdin`, выполняет операцию и печатает ответ JSON в `stdout`

## Контракт JSON

### Запрос
```json
{
  "task": "add|mul|pow",
  "a": 2,
  "b": 3
}
```

### Ответ
Успех:
```json
{ "result": 5 }
```
Ошибка:
```json
{ "error": "unknown task: ..." }
```

## Как запустить

### 1) Go (напрямую, stdin/stdout)
Выполняйте из папки `mid4/go`:
```powershell
echo '{"task":"add","a":2,"b":3}' | go run .
```

### 2) Python (который дергает Go)
Из корня `lab9`:
```powershell
py mid4\python\main.py --task add --a 2 --b 3
```

Также можно передать “сырое” JSON через stdin:
```powershell
echo '{"task":"mul","a":4,"b":5}' | py mid4\python\main.py
```

## Тесты (pytest)
Из корня `lab9`:
```powershell
py -m pytest -q mid4\tests
```

Тесты проверяют парсинг/обработку и работу функции `run_go()` (через mock subprocess).

## mid2: Текстовый протокол + фоновые горутины

Проект демонстрирует обмен данными между Python и Go без JSON:

- Python отправляет запрос в Go через `stdin` в формате `"<task> <a> <b>"`
- Go читает текст из `stdin`, выполняет операцию в **worker goroutine**, и печатает результат в `stdout`
- Сообщения, показывающие работу горутины, печатаются в `stderr`

### Протокол

Запрос (stdin):
```text
add 2 3
```

Ответ (stdout):
- Успех: число (например `5`)
- Ошибка: строка вида `ERROR ...`

### Как запустить

1) Go (напрямую, stdin/stdout)
Из папки `mid2/go`:
```powershell
echo "add 2 3" | go run .
```

2) Python (который дергает Go)
Из корня `lab9`:
```powershell
py mid2\python\main.py --task add --a 2 --b 3
```

Можно также передать запрос “сырым” текстом через stdin:
```powershell
echo "mul 4 5" | py mid2\python\main.py
```

Чтобы гарантированно увидеть сообщения про горутину (stderr), можно слить stderr в stdout:
```powershell
py mid2\python\main.py --task add --a 2 --b 3 2>&1
```

Ожидаемые строки:
- `[main goroutine] dispatching job`
- `[worker goroutine] started`
- `[worker goroutine] processing task: add`

### Тесты (pytest)
Из корня `lab9`:
```powershell
py -m pytest -q mid2\tests
```



## mid9: Сравнение скорости выполнения Rust и Python (решето Эратосфена)

Проект демонстрирует сравнение производительности реализации решета Эратосфена на Rust и Python.

### Структура проекта

```
mid9/
├── rust/                 # Rust реализация
│   ├── Cargo.toml
│   └── src/
│       ├── lib.rs       (функции решета)
│       └── main.rs      (бенчмарк-бинарник)
├── python/              # Python реализация
│   └── sieve.py
├── tests/               # Тесты pytest
│   └── test_sieve.py
├── benchmark.py         # Скрипт сравнения
└── .gitignore
```

### Реализованные функции

- `sieve_of_eratosthenes(n)` – возвращает вектор/список булевых значений, где `is_prime[i] = True`, если i простое.
- `primes_upto(n)` – возвращает список простых чисел до n.
- `count_primes(n)` – возвращает количество простых чисел до n.

### Запуск тестов

#### Python тесты (pytest)
```powershell
cd mid9
py -m pytest tests/ -v
```

#### Rust тесты (cargo test)
```powershell
cd mid9/rust
cargo test
```

### Бенчмарк сравнения

Скрипт `benchmark.py` автоматически компилирует Rust проект (release) и запускает обе реализации, сравнивая среднее время выполнения.

```powershell
cd mid9
py benchmark.py -n 1000000 --iterations 10
```

Параметры:
- `-n` – верхняя граница решета (по умолчанию 1 000 000)
- `--iterations` – количество итераций для усреднения (по умолчанию 10)

Пример вывода:
```
Бенчмарк решета Эратосфена до n = 1000000
Итераций: 10

Запуск Python...
Python среднее время: 0.123456 сек
Запуск Rust...
Rust среднее время: 0.012345 сек
Ускорение Rust относительно Python: 10.00x
```

### Результаты сравнения

На тестовых запусках (n=1 000 000) Rust показывает ускорение в 4–10 раз относительно чистой Python реализации, в зависимости от оптимизаций и окружения.

### Принципы чистого кода

- Четкое разделение ответственности (отдельные модули для Rust и Python)
- Документированные функции (docstrings на Python, /// на Rust)
- Юнит-тесты для обеих реализаций
- Использование типизированных аргументов (type hints в Python, явные типы в Rust)
- Обработка ошибок и граничных случаев (n < 2 и т.п.)

### Атомарные коммиты

Проект размещён в Git с атомарными коммитами:
- `feat: add Rust implementation of sieve of Eratosthenes`
- `feat: add Python implementation of sieve of Eratosthenes`
- `feat: add benchmark script for Rust vs Python comparison`
- `test: add pytest tests for sieve functions`
- `chore: add .gitignore for mid9 project`

### Заключение

Проект наглядно демонстрирует преимущества компилируемых языков (Rust) над интерпретируемыми (Python) в задачах интенсивных вычислений. Реализация может быть расширена для сравнения с другими алгоритмами или языками.

---
