from .base_exceptions import MediaError

class MovieError(MediaError):
    """Base exception for movie operations."""
    pass

class SeriesError(MediaError):
    """Base exception for series operations."""
    pass

class TitleLenghtInvalid(MediaError):
    """Title doesn't meet the minimum length for search purposes."""
    pass

class TitleTypeInvalid(MediaError):
    """Raised when a show type is invalid."""
    pass

class RatingInvalid(MediaError):
    """Raised when a given rating is invalid."""
    pass