class NotFoundError(Exception):
    """Raised when an entity is not found by the repository/service layer."""

    def __init__(self, entity: str, identifier: object):
        self.entity = entity
        self.identifier = identifier
        super().__init__(f"{entity} with id={identifier!r} not found")


class InvalidCredentialsError(Exception):
    """Raised by AuthService when a username/password pair fails to authenticate."""

    def __init__(self):
        super().__init__("Invalid username or password")
