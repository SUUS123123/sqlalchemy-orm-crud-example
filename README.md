# SQLAlchemy ORM CRUD Example

A compact SQLAlchemy 2.x example based on typed ORM models, `Session`, CRUD operations, and the Repository pattern. SQLite runs in memory, so no database server or configuration is needed.

## Run

```powershell
python -m pip install -r requirements.txt
python sqlalchemy_orm_crud.py
```

The program creates a product, reads it by ID, lists products, updates its price, deletes it, and prints the resulting values.
