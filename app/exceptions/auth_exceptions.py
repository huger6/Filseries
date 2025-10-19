from .base_exceptions import MediaError

class RegisterError(MediaError):
    """An error has occurred during register."""
    pass

class LoginError(MediaError):
    """An error has occurred during login."""
    pass