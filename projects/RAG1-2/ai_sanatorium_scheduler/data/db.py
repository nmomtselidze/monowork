from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ai_sanatorium_scheduler.config.settings import settings

# Create engine and session maker for PostgreSQL
engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db():
    """Yield a SQLAlchemy session (FastAPI dependency style)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
