import os
import sys
from pathlib import Path

# Use SQLite in-memory DB for tests (overrides PostgreSQL default before any import)
os.environ["DATABASE_URL"] = "sqlite:///./test_fintech.db"

# Add repo root so 'backend' package is importable
sys.path.insert(0, str(Path(__file__).parent.parent))
# Add backend/ so relative imports inside backend (models, database, extraction) work
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import pytest
from database import init_db, engine, Base

@pytest.fixture(autouse=True, scope="session")
def setup_db():
    """Create all tables in the test SQLite DB before the session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
