"""
Validations for watchlist and seen/progress operations.
Handles validation for both movies and TV series.
"""
from typing import Optional
from app.exceptions import StatusError, StatusUnchanged, StatusInvalidToChange


def validate_title_id(title_id: Optional[int]) -> None:
    """
    Validate that a title ID is provided and is a positive integer.
    
    Args:
        title_id: The ID of the movie or series from the API
        
    Raises:
        StatusError: If the ID is missing or invalid
    """
    if title_id is None:
        raise StatusError("Title ID is required")
    
    if not isinstance(title_id, int):
        try:
            title_id = int(title_id)
        except (ValueError, TypeError):
            raise StatusError("Title ID must be a valid number")
    
    if title_id <= 0:
        raise StatusError("Title ID must be a positive number")


def validate_season_number(season_number: Optional[int], max_seasons: Optional[int] = None) -> None:
    """
    Validate that a season number is valid.
    
    Args:
        season_number: The season number to validate
        max_seasons: Optional maximum number of seasons for the series
        
    Raises:
        StatusError: If the season number is invalid
    """
    if season_number is None:
        raise StatusError("Season number is required")
    
    if not isinstance(season_number, int):
        try:
            season_number = int(season_number)
        except (ValueError, TypeError):
            raise StatusError("Season number must be a valid number")
    
    if season_number < 0:
        raise StatusError("Season number cannot be negative")
    
    if max_seasons is not None and season_number > max_seasons:
        raise StatusError(f"Season number cannot exceed {max_seasons}")


def validate_rating(rating: Optional[float]) -> None:
    """
    Validate that a rating is within acceptable bounds (0-10).
    
    Args:
        rating: The rating value to validate
        
    Raises:
        StatusError: If the rating is invalid
    """
    if rating is None:
        raise StatusError("Rating is required")
    
    try:
        rating = float(rating)
    except (ValueError, TypeError):
        raise StatusError("Rating must be a valid number")
    
    if rating < 0 or rating > 10:
        raise StatusError("Rating must be between 0 and 10")


def validate_can_add_to_seen(already_seen: bool) -> None:
    """
    Validate that a title can be added to seen list.
    
    Args:
        already_seen: Whether the title is already marked as seen
        
    Raises:
        StatusUnchanged: If the title is already in the seen list
    """
    if already_seen:
        raise StatusUnchanged("This title is already marked as seen")


def validate_can_add_to_watchlist(already_in_watchlist: bool, already_seen: bool) -> None:
    """
    Validate that a title can be added to watchlist.
    
    Args:
        already_in_watchlist: Whether the title is already in the watchlist
        already_seen: Whether the title is already marked as seen
        
    Raises:
        StatusUnchanged: If the title is already in the watchlist
        StatusInvalidToChange: If the title is already marked as seen
    """
    if already_in_watchlist:
        raise StatusUnchanged("This title is already in your watchlist")
    
    if already_seen:
        raise StatusInvalidToChange("Cannot add to watchlist - this title is already marked as seen")


def validate_can_remove_from_seen(is_seen: bool) -> None:
    """
    Validate that a title can be removed from seen list.
    
    Args:
        is_seen: Whether the title is currently marked as seen
        
    Raises:
        StatusError: If the title is not in the seen list
    """
    if not is_seen:
        raise StatusError("This title is not in your seen list")


def validate_can_remove_from_watchlist(is_in_watchlist: bool) -> None:
    """
    Validate that a title can be removed from watchlist.
    
    Args:
        is_in_watchlist: Whether the title is currently in the watchlist
        
    Raises:
        StatusError: If the title is not in the watchlist
    """
    if not is_in_watchlist:
        raise StatusError("This title is not in your watchlist")
