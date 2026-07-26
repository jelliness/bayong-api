from app.core.security import verify_password
from app.models.enums import UserRole
from app.repositories.category_repository import CategoryRepository
from app.repositories.price_repository import PriceRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.store_repository import StoreRepository
from app.repositories.user_repository import UserRepository
from seed.seeder import Seeder


def test_run_creates_categories_stores_products_and_prices(db_session):
    Seeder(db_session).run()

    categories = CategoryRepository(db_session).list(limit=100)
    stores = StoreRepository(db_session).list(limit=100)
    products = ProductRepository(db_session).list_with_filters(limit=100)
    prices = PriceRepository(db_session).list(limit=1000)

    assert len(categories) == 3
    assert len(stores) == 4
    assert len(products) == 10
    assert len(prices) > 0


def test_run_creates_an_admin_user(db_session):
    Seeder(db_session).run()

    admin = UserRepository(db_session).get_by_username(Seeder.ADMIN_USERNAME)

    assert admin is not None
    assert admin.role == UserRole.ADMIN
    assert verify_password(Seeder.ADMIN_PASSWORD, admin.hashed_password) is True


def test_run_is_idempotent_for_admin_categories_stores_and_products(db_session):
    seeder = Seeder(db_session)
    seeder.run()
    seeder.run()

    categories = CategoryRepository(db_session).list(limit=100)
    stores = StoreRepository(db_session).list(limit=100)
    products = ProductRepository(db_session).list_with_filters(limit=100)
    users = UserRepository(db_session).list(limit=100)

    assert len(categories) == 3
    assert len(stores) == 4
    assert len(products) == 10
    assert len(users) == 1


def test_each_product_gets_prices_from_three_or_four_stores(db_session):
    Seeder(db_session).run()

    products = ProductRepository(db_session).list_with_filters(limit=100)
    price_repo = PriceRepository(db_session)

    for product in products:
        prices = price_repo.list_by_product(product.id)
        assert len(prices) in (3, 4)
