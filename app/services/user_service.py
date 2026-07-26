from typing import Optional

from app.core.security import hash_password
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_by_username(self, username: str) -> Optional[User]:
        return self.user_repository.get_by_username(username)

    def create(self, username: str, password: str, role: UserRole = UserRole.ADMIN) -> User:
        return self.user_repository.create(
            {"username": username, "hashed_password": hash_password(password), "role": role}
        )
