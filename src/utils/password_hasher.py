import bcrypt


class PasswordHasher:
    salt: bytes

    def __init__(self) -> None:
        self.salt = bcrypt.gensalt()

    def encode(self, pwd: str) -> bytes:
        return pwd.encode("utf-8")

    def decode(self, pwd: bytes) -> str:
        return pwd.decode("utf-8")

    def hash_password(self, password: str) -> bytes:
        return self.decode(bcrypt.hashpw(self.encode(password), self.salt))

    def compare_password(self, encrypted_password: str, plain_password: str):
        return bcrypt.checkpw(
            self.encode(plain_password), self.encode(encrypted_password)
        )
