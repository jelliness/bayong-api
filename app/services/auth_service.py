from app.core.exceptions import InvalidCredentialsError
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.services.user_service import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def authenticate(self, username: str, password: str) -> User:
        user = self.user_service.get_by_username(username)
        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()
        return user

    def create_token(self, user: User) -> str:
        return create_access_token(subject=user.username, role=user.role.value)
