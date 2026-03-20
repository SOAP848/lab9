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


