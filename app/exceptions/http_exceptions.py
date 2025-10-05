from .base_exceptions import MediaError

class AcessDenied(MediaError):
    """403 HTTP error."""
    pass