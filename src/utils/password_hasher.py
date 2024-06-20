import bcrypt


class PasswordHasher:
    salt: bytes

    def __init__(self) -> None:
        self.salt = bcrypt.gensalt()

    def encode(self, pwd: str) -> str:
        return pwd.encode("utf-8")

    def hash_password(self, password: str) -> str:
        return str(bcrypt.hashpw(self.encode(password), self.salt))
