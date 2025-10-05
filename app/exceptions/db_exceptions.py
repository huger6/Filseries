from .base_exceptions import MediaError

class DatabaseError(MediaError):
    """Base exception for all database interaction/table creations."""
    pass

class DatabaseNotFound(DatabaseError):
    """Raised when .db file path doesn't work, doesn't exist or is None."""
    pass

class TablesMissingError(DatabaseError):
    """Raised when an important table is missing from the database."""
    pass
