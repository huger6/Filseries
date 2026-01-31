from app.models.user import User
from app.extensions import bcrypt
from app.exceptions import RegisterError, LoginError, AuthError
from app.constants import PASSWORD_PATTERN, USERNAME_PATTERN, NAME_PATTERN
from app.services.db import username_available
import re

def validateUsername(username):
    if not isinstance(username, str):
        return False
    username = username.strip()
    if not username:
        return False
    return bool(re.fullmatch(USERNAME_PATTERN, username))

def validateName(name):
    if not isinstance(name, str):
        return False
    
    name = name.strip()

    return bool(re.fullmatch(NAME_PATTERN, name))

def validatePassword(pw):
    if not isinstance(pw, str):
        return False
    if not pw:
        return False
    return bool(re.fullmatch(PASSWORD_PATTERN, pw))

def validatePasswordConfirm(pw, pw_confirm):
    if not isinstance(pw, str) or not isinstance(pw_confirm, str):
        return False
    return pw == pw_confirm

def validateRegister(username, name, pw, pw_confirm):
    username_exists = User.query.filter_by(username=username).first()
    if username_exists:
        raise RegisterError("This username already exists!")
    
    # Need some rework here 
    return validateName(name) and validateUsername(username) and validatePassword(pw) and validatePasswordConfirm(pw, pw_confirm)

def validateLogin(username, pw):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise LoginError("Invalid credentials!")
    
    if not bcrypt.check_password_hash(user.pass_hash, pw):
        raise LoginError("Invalid credentials 2!")

    return user

def validateChangeUsername(user_id, new_username):
    if not validateUsername(new_username):
        raise AuthError("Invalid username")

    username_found = username_available(new_username)
    if username_found:
        raise AuthError("Username already exists")
    
    return True
    