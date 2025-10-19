from app.models.user import User
from app.extensions import bcrypt
from app.exceptions import RegisterError, LoginError

def validateEmail(email):
    return True

def validateUsername(username):
    return True

def validateName(name):
    return True

def validatePassword(pw):
    return True

def validatePasswordConfirm(pw, pw_confirm):
    return True

def validateRegister(username, name, pw, pw_confirm, email : None):
    username_exists = User.query.filter_by(username).first()
    if username_exists:
        raise RegisterError("The username already exists!")
    if (email is None):
        return validateName(name) and validateUsername(username) and validatePassword(pw) and validatePasswordConfirm(pw, pw_confirm)
    return validateName(name) and validateUsername(username) and validatePassword(pw) and validatePasswordConfirm(pw, pw_confirm) and validateEmail(email)

def validateLogin(username, pw):
    user = User.query.filter_by(username).first()
    if not user:
        raise LoginError("Username not found!")
    
    if not bcrypt.check_password_hash(user.pass_hash, pw):
        raise LoginError("Password is incorrect!")

    return True