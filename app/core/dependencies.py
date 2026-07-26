import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.repositories.price_history_repository import PriceHistoryRepository
from app.repositories.price_repository import PriceRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.store_repository import StoreRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.category_service import CategoryService
from app.services.price_comparison_service import PriceComparisonService
from app.services.price_service import PriceService
from app.services.product_service import ProductService
from app.services.store_service import StoreService
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(CategoryRepository(db))


def get_store_service(db: Session = Depends(get_db)) -> StoreService:
    return StoreService(StoreRepository(db))


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(db))


def get_price_service(db: Session = Depends(get_db)) -> PriceService:
    return PriceService(PriceRepository(db), PriceHistoryRepository(db))


def get_price_comparison_service(db: Session = Depends(get_db)) -> PriceComparisonService:
    return PriceComparisonService(ProductRepository(db), PriceRepository(db), PriceHistoryRepository(db))


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserService(UserRepository(db)))


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
    except jwt.InvalidTokenError:
        raise credentials_exception

    username = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = UserRepository(db).get_by_username(username)
    if user is None:
        raise credentials_exception
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return current_user
