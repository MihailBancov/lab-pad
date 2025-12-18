import os
import sys
from pathlib import Path

# Ensure service-local imports like `import app...` resolve.
SERVICE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVICE_ROOT))

# Required by pydantic-settings at import time
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://user:pass@localhost:5432/test")
os.environ.setdefault("JWT_SECRET", "unit-test-secret")
os.environ.setdefault("SERVICE_NAME", "auth-service")
os.environ.setdefault("PORT", "8001")
os.environ.setdefault("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
