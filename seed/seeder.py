import random
from datetime import date
from decimal import Decimal
from typing import List

from sqlalchemy.orm import Session

from app.models.enums import PriceSource, SizeUnit
from app.models.store import Store
from app.repositories.category_repository import CategoryRepository
from app.repositories.price_repository import PriceRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.store_repository import StoreRepository
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


class Seeder:
    """Populates an admin user, categories, stores, ~10 products, and per-store prices for local dev."""

    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "ChangeMe123!"  # local/dev only - rotate before any real deployment

    CATEGORIES = [
        {"category_name": "Beverages", "parent_category": None},
        {"category_name": "Snacks", "parent_category": None},
        {"category_name": "Household", "parent_category": None},
    ]

    STORES = [
        dict(
            store_name="MegaMart",
            branch="Ortigas",
            city="Pasig",
            province="Metro Manila",
            region="NCR",
            store_type="supermarket",
            has_membership=False,
        ),
        dict(
            store_name="ValueStore",
            branch="Quezon Ave",
            city="Quezon City",
            province="Metro Manila",
            region="NCR",
            store_type="convenience",
            has_membership=False,
        ),
        dict(
            store_name="WholesaleClub",
            branch="BGC",
            city="Taguig",
            province="Metro Manila",
            region="NCR",
            store_type="wholesale",
            has_membership=True,
        ),
        dict(
            store_name="CornerShop",
            branch="Marikina",
            city="Marikina",
            province="Metro Manila",
            region="NCR",
            store_type="sari-sari",
            has_membership=False,
        ),
    ]

    PRODUCTS = [
        dict(
            category="Beverages",
            subcategory="Soft Drinks",
            product_name="Cola Classic",
            brand="FizzCo",
            package_type="bottle",
            size_value=Decimal("1.5"),
            size_unit=SizeUnit.L,
            standard_unit="L",
            standard_quantity=Decimal("1.5"),
            tags={"vegan": True, "gluten_free": True, "halal": True},
            base_price=Decimal("65.00"),
        ),
        dict(
            category="Beverages",
            subcategory="Juice",
            product_name="Orange Juice",
            brand="Sunburst",
            package_type="carton",
            size_value=Decimal("1"),
            size_unit=SizeUnit.L,
            standard_unit="L",
            standard_quantity=Decimal("1"),
            tags={"vegan": True, "gluten_free": True},
            base_price=Decimal("95.00"),
        ),
        dict(
            category="Beverages",
            subcategory="Water",
            product_name="Purified Water",
            brand="AquaPure",
            package_type="bottle",
            size_value=Decimal("500"),
            size_unit=SizeUnit.ML,
            standard_unit="L",
            standard_quantity=Decimal("0.5"),
            tags={"vegan": True},
            base_price=Decimal("15.00"),
        ),
        dict(
            category="Snacks",
            subcategory="Chips",
            product_name="Potato Chips Original",
            brand="Crispo",
            package_type="bag",
            size_value=Decimal("150"),
            size_unit=SizeUnit.G,
            standard_unit="g",
            standard_quantity=Decimal("150"),
            tags={"vegan": True, "gluten_free": False},
            base_price=Decimal("55.00"),
        ),
        dict(
            category="Snacks",
            subcategory="Biscuits",
            product_name="Choco Sandwich Cookies",
            brand="Snackrite",
            package_type="pack",
            size_value=Decimal("300"),
            size_unit=SizeUnit.G,
            standard_unit="g",
            standard_quantity=Decimal("300"),
            tags={"vegan": False},
            base_price=Decimal("48.00"),
        ),
        dict(
            category="Snacks",
            subcategory="Nuts",
            product_name="Roasted Peanuts",
            brand="NuttyBite",
            package_type="pack",
            size_value=Decimal("200"),
            size_unit=SizeUnit.G,
            standard_unit="g",
            standard_quantity=Decimal("200"),
            tags={"vegan": True, "gluten_free": True, "halal": True},
            base_price=Decimal("70.00"),
        ),
        dict(
            category="Snacks",
            subcategory="Candy",
            product_name="Fruit Gummy Candy",
            brand="Chewz",
            package_type="sachet",
            size_value=Decimal("100"),
            size_unit=SizeUnit.SACHETS,
            standard_unit="g",
            standard_quantity=Decimal("100"),
            tags={"vegan": True, "halal": True},
            base_price=Decimal("35.00"),
        ),
        dict(
            category="Household",
            subcategory="Cleaning",
            product_name="Dish Washing Liquid",
            brand="Sparkle",
            package_type="bottle",
            size_value=Decimal("500"),
            size_unit=SizeUnit.ML,
            standard_unit="mL",
            standard_quantity=Decimal("500"),
            tags={"vegan": False},
            base_price=Decimal("85.00"),
        ),
        dict(
            category="Household",
            subcategory="Paper Goods",
            product_name="Toilet Paper 12-Roll",
            brand="Softly",
            package_type="pack",
            size_value=Decimal("12"),
            size_unit=SizeUnit.ROLLS,
            standard_unit="rolls",
            standard_quantity=Decimal("12"),
            tags={},
            base_price=Decimal("210.00"),
        ),
        dict(
            category="Household",
            subcategory="Laundry",
            product_name="Laundry Detergent Powder",
            brand="CleanWave",
            package_type="pack",
            size_value=Decimal("1"),
            size_unit=SizeUnit.KG,
            standard_unit="kg",
            standard_quantity=Decimal("1"),
            tags={},
            base_price=Decimal("120.00"),
        ),
    ]

    PRICE_VARIANCE = [Decimal("-5.00"), Decimal("0.00"), Decimal("3.50"), Decimal("7.25"), Decimal("-2.75")]

    def __init__(self, db: Session, random_seed: int = 42):
        self.db = db
        self.category_repository = CategoryRepository(db)
        self.store_repository = StoreRepository(db)
        self.product_repository = ProductRepository(db)
        self.price_repository = PriceRepository(db)
        self.user_service = UserService(UserRepository(db))
        self._random = random.Random(random_seed)

    def run(self) -> None:
        self._seed_admin_user()
        self._seed_categories()
        stores = self._seed_stores()
        self._seed_products_and_prices(stores)

    def _seed_admin_user(self) -> None:
        if not self.user_service.get_by_username(self.ADMIN_USERNAME):
            self.user_service.create(self.ADMIN_USERNAME, self.ADMIN_PASSWORD)

    def _seed_categories(self) -> None:
        for payload in self.CATEGORIES:
            if not self.category_repository.get_by_name(payload["category_name"]):
                self.category_repository.create(payload)

    def _seed_stores(self) -> List[Store]:
        existing_by_name = {s.store_name: s for s in self.store_repository.list(limit=1000)}
        stores = []
        for payload in self.STORES:
            store = existing_by_name.get(payload["store_name"]) or self.store_repository.create(payload)
            stores.append(store)
        return stores

    def _seed_products_and_prices(self, stores: List[Store]) -> None:
        existing_names = {p.product_name for p in self.product_repository.list_with_filters(limit=1000)}
        for spec in self.PRODUCTS:
            spec = dict(spec)
            base_price = spec.pop("base_price")
            if spec["product_name"] in existing_names:
                continue

            product = self.product_repository.create(
                {
                    **spec,
                    "last_verified": date.today(),
                    "availability": True,
                    "active": True,
                    "private_label": False,
                    "organic": False,
                }
            )

            chosen_stores = self._random.sample(stores, k=self._random.choice([3, 4]))
            for store in chosen_stores:
                self._create_price_for(product.id, store, base_price)

    def _create_price_for(self, product_id: int, store: Store, base_price: Decimal) -> None:
        variance = self._random.choice(self.PRICE_VARIANCE)
        price_value = (base_price + variance).quantize(Decimal("0.01"))
        is_promo = self._random.random() < 0.3
        sale_price = (price_value * Decimal("0.9")).quantize(Decimal("0.01")) if is_promo else None

        self.price_repository.create(
            {
                "product_id": product_id,
                "store_id": store.id,
                "price": price_value,
                "sale_price": sale_price,
                "is_promo": is_promo,
                "promo_type": "discount" if is_promo else None,
                "membership_required": store.has_membership,
                "date_collected": date.today(),
                "price_source": PriceSource.MANUAL,
            }
        )
