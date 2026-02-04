from urllib.parse import urlparse
from app import app

def enpoint_is_valid(endpoint):
    """Check if the endpoint name is a valid Flask endpoint."""
    return endpoint in app.view_functions

def is_safe_url(url):
    """
    Check if the URL is safe for redirection.
    Only allows relative URLs that start with '/' and don't contain
    protocol schemes or external domains.
    """
    if not url:
        return False
    
    # Must start with a single forward slash (relative path)
    if not url.startswith('/'):
        return False
    
    # Prevent protocol-relative URLs (//example.com)
    if url.startswith('//'):
        return False
    
    # Parse the URL to check for any suspicious components
    parsed = urlparse(url)
    
    # Should not have a scheme (http, https, javascript, etc.)
    if parsed.scheme:
        return False
    
    # Should not have a netloc (domain)
    if parsed.netloc:
        return False
    
    return True
