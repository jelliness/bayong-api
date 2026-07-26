from app.core.database import SessionLocal
from seed.seeder import Seeder


def main() -> None:
    db = SessionLocal()
    try:
        Seeder(db).run()
        print("Seed data loaded.")
        print(
            f"Admin login -> username: {Seeder.ADMIN_USERNAME}, password: {Seeder.ADMIN_PASSWORD} "
            "(local/dev only, change before any real deployment)"
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
