from app.routes.main import main_bp
from app.routes.auth import auth_bp
from app.routes.watchlist import watchlist_bp
from app.routes.watched import watched_bp
from app.routes.titles import titles_bp
from app.routes.error_handler import error_handler_bp

blueprints = [main_bp, auth_bp, watchlist_bp, watched_bp, titles_bp, error_handler_bp]