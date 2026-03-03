from passlib.context import CryptContext

crypt = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str):
    return crypt.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt.verify(plain_password, hashed_password)