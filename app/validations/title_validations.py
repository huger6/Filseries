from typing import List, Tuple, Optional
#Constants
from app.constants import CURRENT_YEAR
from app.constants import MIN_TITLE_LENGTH, MAX_TITLE_LENGTH
from app.constants import MIN_LIM_PER_PAGE, LIMIT_PER_PAGE
from app.constants import SORT_BY_FILTERS, SORT_BY_ORDERS
from app.constants import GENRES_ALLOWED
#Exceptions
from app.exceptions import TitleLengthInvalid, SearchError

def validate_title(title: str) -> None:
    """Validate that the title length is within acceptable bounds."""
    if title is None or len(title.strip()) == 0:
        raise TitleLengthInvalid("Please enter a search term")
    if len(title.strip()) < MIN_TITLE_LENGTH:
        raise TitleLengthInvalid(f"Search term must be at least {MIN_TITLE_LENGTH} characters")
    if len(title.strip()) >= MAX_TITLE_LENGTH:
        raise TitleLengthInvalid(f"Search term is too long (max {MAX_TITLE_LENGTH - 1} characters)")

def validate_page(page: int) -> None:
    """Validate that the page number is valid."""
    if page < 1:
        raise SearchError(f"Page '{page}' is invalid")

def validate_limit_per_page(limit: int) -> None:
    """Validate that the limit per page is within acceptable bounds."""
    if not MIN_LIM_PER_PAGE <= limit <= LIMIT_PER_PAGE:
        raise SearchError(f"Limit per page is invalid: {limit}")

def validate_sort_by(sort_by: Tuple[str, str]) -> None:
    """Validate that the sort by filter and order are supported."""
    if sort_by[0] not in SORT_BY_FILTERS:
        raise SearchError(f"Sorting method isn't supported: {sort_by[0]}")
    if sort_by[1] not in SORT_BY_ORDERS:
        raise SearchError(f"Sorting order isn't supported: {sort_by[1]}")

def validate_genres(genres: List[str]) -> List[str]:
    """Validate and filter genres, returning only valid ones."""
    return [genre for genre in genres if genre in GENRES_ALLOWED]

def validate_years(years: Optional[List[int]]) -> None:
    """Validate that the years interval is valid."""
    if years:
        if len(years) != 2:
            raise SearchError("Year's interval is invalid")
        for year in years:
            if year > CURRENT_YEAR:
                raise SearchError(f"Year({year}) is bigger than the current year({CURRENT_YEAR})")

def validate_ratings(ratings: Optional[List[float]]) -> None:
    """Validate that the ratings range is valid."""
    if ratings:
        if not (0 <= ratings[0] <= 10 and 0 <= ratings[1] <= 10):
            raise SearchError("Ratings must be 0-10")