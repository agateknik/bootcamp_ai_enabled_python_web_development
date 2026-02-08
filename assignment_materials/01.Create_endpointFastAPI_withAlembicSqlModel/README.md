## ASSIGNMENT 1

#### Membuat endpoint dengan fast API menggunakan database Sqlite juga SQLmodel ORM, dan Alembic migration manager

- 2 endpoint @min (get, post)

```
uv init

uv add uvicorn fastapi scalar-fastapi pydantic pydantic-settings alembic sqlmodel

uv run uvicorn app.main:app --reload
```
