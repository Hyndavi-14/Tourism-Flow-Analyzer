import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

def get_engine():
    # Load once, read from .env
    load_dotenv()
    user = os.getenv("PG_USER")
    pwd  = os.getenv("PG_PASSWORD")
    host = os.getenv("PG_HOST", "localhost")
    port = os.getenv("PG_PORT", "5432")
    db   = os.getenv("PG_DB")

    url = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"
    return create_engine(url, future=True)