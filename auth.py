# auth.py
import bcrypt
from db import get_user, add_user

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

def signup(username: str, password: str):
    if get_user(username):
        return False, "Username already exists."
    add_user(username, hash_password(password))
    return True, "Account created. Please log in."

def login(username: str, password: str):
    u = get_user(username)
    if not u:
        return False, "User not found."
    if not verify_password(password, u["password_hash"]):
        return False, "Invalid password."
    return True, u
