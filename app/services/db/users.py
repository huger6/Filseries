from app.extensions import db
from app.extensions import bcrypt
from sqlalchemy import text

# ============================================================
# User Account Management
# ============================================================

def register_new_user(username: str, name: str, pw: str):
    """
    Creates a new user account with hashed password.
    Returns True on success, False on failure (e.g., duplicate username).
    """
    if not username or not name or not pw:
        return False
    
    hashed_password = bcrypt.generate_password_hash(pw).decode("utf-8")
    try:
        db.session.execute(
            text("INSERT INTO users (name, username, pass_hash) VALUES (:name, :username, :pass_hash)"), 
            {"name": name, "username": username, "pass_hash": hashed_password}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False

    return True

def change_user_password(user_id: int, new_pw: str):
    """
    Updates the user's password with a new hashed password.
    """
    if not user_id or not new_pw:
        return False
    
    hashed_password = bcrypt.generate_password_hash(new_pw).decode("utf-8")
    try:
        db.session.execute(
            text("UPDATE users SET pass_hash=:pass_hash WHERE id=:user_id"),
            {"pass_hash": hashed_password, "user_id": user_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def change_user_username(user_id: int, new_username: str):
    """
    Updates the user's username.
    Should check availability before calling this function.
    """
    if not user_id or not new_username:
        return False
    
    try:
        db.session.execute(
            text("UPDATE users SET username=:new_username WHERE id=:user_id"),
            {"new_username": new_username, "user_id": user_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def username_available(username: str):
    """
    Checks if a username is available for registration or change.
    Returns True if available, False if taken or on error.
    """
    if not username:
        return False
    
    try:
        result = db.session.execute(
            text("SELECT username FROM users WHERE username=:username"),
            {"username": username}
        )
        row = result.first()
        return row is None
    except Exception:
        return False

def get_user_pfp(user_id: int):
    """
    Retrieves the user's profile picture binary data.
    Returns None if no picture is set or on error.
    """
    if not user_id:
        return None
    try:
        result = db.session.execute(
            text("SELECT pfp FROM users WHERE id=:user_id"),
            {"user_id": user_id}
        )
        row = result.first()
        if row and row.pfp:
            return row.pfp
        return None
    except Exception:
        return None

def update_user_pfp(user_id: int, pfp_data: bytes):
    """
    Updates the user's profile picture.
    Accepts binary image data (MEDIUMBLOB, max ~16MB).
    """
    if not user_id or not pfp_data:
        return False
    try:
        db.session.execute(
            text("UPDATE users SET pfp=:pfp WHERE id=:user_id"),
            {"pfp": pfp_data, "user_id": user_id}
        )
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False

