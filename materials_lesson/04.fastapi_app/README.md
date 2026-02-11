### Meeting 3

in this section:

1. we learn about setup linter for pyhton using Ruff

    ```
    install ruff:
    uv add ruff --dev


    cek lint:
    uv run ruff check

    fix error lint format:
    uv run ruff check --fix --unsafe-fixes
    ```

    Run on browser
    ```
    uv run uvicorn app.main:app --reload
    ```
    - Setup ruff on pyproject.toml , all about ruff see on [documentation](https://docs.astral.sh/ruff/)

2. Then, practical FastAPI with SQLMODEL ORM and Alembic use sqlite db.

    - script/seeder.py is script for seed db made by AI, run with command : uv run script/seeder.py
    - logic_return_date.py is explanation about logic function is_available() on models.py

Thanks