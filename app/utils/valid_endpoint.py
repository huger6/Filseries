from app import app

def enpoint_is_valid(endpoint):
    return endpoint in app.view_functions
