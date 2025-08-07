#  Инструкция по запуску проекта

## 1 Вариант запуска

1. В корне проекта выполните:

```bash
docker-compose up --build
```

2. Приложение будет доступно по адресу:

- http://localhost:8000

3. База данных (PostgreSQL):

- Хост: `localhost`
- Порт: `5432`
- Пользователь: `postgres`
- Пароль: `postgres`

---

## 2 Вариант запуска

1. Установите Python 3.11+

2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Убедитесь, что PostgreSQL доступен по:

```
postgresql://postgres:postgres@localhost:5432/postgres
```

5. Примените миграции:

```bash
alembic upgrade head
```

6. Запустите сервер:

```bash
uvicorn main:app --reload
```

---

##  Пользователи по умолчанию (создаются при миграции)

Администратор | `admin@example.com` | `admin123` |
Пользователь   | `user@example.com`  | `user123`  |

# Рекомендую проверить LF у entrypoint.sh
