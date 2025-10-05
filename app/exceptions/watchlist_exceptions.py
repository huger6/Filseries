from .base_exceptions import MediaError

class StatusError(MediaError):
    """Base exception for status-related errors."""
    pass

class StatusUnchanged(StatusError):
    """Raised when trying to add a status that already exists."""
    pass

class StatusInvalidToChange(StatusError):
    """Raised when trying to add 'to_watch' when current status is 'watched'."""
    pass
