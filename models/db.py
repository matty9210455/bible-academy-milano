from sqlalchemy import create_engine
from config import DATABASE_URL

_engine = None

def get_connection():
    global _engine
    if _engine is None:
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL non configurato")
        _engine = create_engine(DATABASE_URL)
    return _engine.connect()