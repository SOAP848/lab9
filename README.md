# Лабораторная работа №9 — Вариант 9

# mid4: Python <-> Go через JSON (stdin/stdout)

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

