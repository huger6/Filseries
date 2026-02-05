"""
Validations for pagination operations.
Handles validation for infinite scroll / cursor-based pagination.
"""
from datetime import datetime
from typing import Optional, Tuple
from app.exceptions import StatusError

# Constants for pagination
MIN_LIMIT = 1
MAX_LIMIT = 50
DEFAULT_LIMIT = 30


def validate_pagination_params(
    last_id: Optional[int], 
    last_date: Optional[str], 
    limit: Optional[int]
) -> Tuple[Optional[int], Optional[datetime], int]:
    """
    Validate pagination parameters for cursor-based pagination.
    
    Args:
        last_id: The ID of the last item from previous page
        last_date: The date of the last item (ISO format string)
        limit: Number of results to fetch
        
    Returns:
        Tuple of (validated_last_id, validated_last_date, validated_limit)
        
    Raises:
        StatusError: If validation fails
    """
    validated_limit = DEFAULT_LIMIT
    validated_last_id = None
    validated_last_date = None
    
    # Validate limit
    if limit is not None:
        try:
            validated_limit = int(limit)
            if validated_limit < MIN_LIMIT:
                validated_limit = MIN_LIMIT
            elif validated_limit > MAX_LIMIT:
                validated_limit = MAX_LIMIT
        except (ValueError, TypeError):
            raise StatusError("Invalid limit value")
    
    # Validate last_id
    if last_id is not None:
        try:
            validated_last_id = int(last_id)
            if validated_last_id <= 0:
                raise StatusError("Invalid last_id value: must be positive")
        except (ValueError, TypeError):
            raise StatusError("Invalid last_id value: must be a number")
    
    # Validate last_date
    if last_date is not None:
        try:
            if isinstance(last_date, str):
                # Try parsing ISO format datetime
                validated_last_date = datetime.fromisoformat(last_date.replace('Z', '+00:00'))
            elif isinstance(last_date, datetime):
                validated_last_date = last_date
            else:
                raise StatusError("Invalid last_date format")
        except (ValueError, TypeError):
            raise StatusError("Invalid last_date format: must be ISO format")
    
    # Both last_id and last_date must be provided together for pagination, or neither
    if (validated_last_id is not None) != (validated_last_date is not None):
        raise StatusError("Both last_id and last_date must be provided for pagination")
    
    return validated_last_id, validated_last_date, validated_limit
