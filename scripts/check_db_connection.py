import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlalchemy import create_engine, text  # noqa: E402

from app.core.config import get_settings  # noqa: E402


def main() -> int:
    settings = get_settings()
    engine = create_engine(settings.database_url)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:
        print(f"Database connection FAILED: {exc}")
        return 1

    host_part = settings.database_url.rsplit("@", 1)[-1]
    print(f"Database connection OK: {host_part}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
