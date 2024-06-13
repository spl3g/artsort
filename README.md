# Artsort

# Dependencies
- fastapi
- sqlalchemy
- psycopg2
- alembic
- Jinja2
- uvicorn

# Starting
start postgresql
```sh
alembic upgrade head

fastapi run app/main.py
```
