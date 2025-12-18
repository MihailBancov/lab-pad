import os
import sys
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVICE_ROOT))

os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://user:pass@localhost:5432/test")
os.environ.setdefault("JWT_SECRET", "unit-test-secret")
os.environ.setdefault("SERVICE_NAME", "product-service")
os.environ.setdefault("PORT", "8002")
os.environ.setdefault("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
