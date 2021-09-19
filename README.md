# warships

Консольные кораблики, основанные на сокетах.

## Как играть

### Обязательные требования:

- у обоих игроков должен быть интерпретатор Python >= 3.6
- оба игрока должны быть подключены к одной сети

### Процесс установки игры:

- Оба игрока должны склонировать репозиторий

```
git clone https://github.com/Masynchin/warships.git
```

или скачать по ссылке `https://github.com/Masynchin/warships/archive/refs/heads/main.zip`

- Первый игрок запускает сервер

```
cd warships
python main.py

Сервер - s, клиент - c: s
Подключайтесь к <адрес сервера>
```

- Второй игрок запускает клиент и подключается к серверу

```
cd warships
python main.py

Сервер - s, клиент - c: c
Введите адрес сервера: <адрес сервера>
```
