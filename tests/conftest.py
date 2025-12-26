import pytest
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, inspect

@pytest.fixture(scope="session")
def test_db():
    # Create an in-memory SQLite database for testing
    engine = create_engine('sqlite:///:memory:', echo=False)
    metadata = MetaData()

    # Create test tables
    users = Table('users', metadata,
        Column('id', Integer, primary_key=True),
        Column('username', String),
        Column('email', String),
        comment='User accounts table'
    )

    posts = Table('posts', metadata,
        Column('id', Integer, primary_key=True),
        Column('user_id', Integer, ForeignKey('users.id')),
        Column('title', String),
        Column('content', String),
        comment='User posts table'
    )

    metadata.create_all(engine)

    # Create a database instance and connect it
    from src.database import Database
    db = Database()
    db.engine = engine
    db.db_inspect = inspect(engine)
    db.schemas = ['main']  # SQLite always has 'main' schema
    db.metadata = metadata
    db.table_names = list(metadata.tables.keys())
    db.table_short_names = [table.name for table in metadata.tables.values()]
    db.is_connected = True

    return db
