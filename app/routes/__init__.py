from app.routes.main import main_bp
from app.routes.auth import auth_bp
from app.routes.watchlist import watchlist_bp
from app.routes.titles import titles_bp

blueprints = [main_bp, auth_bp, watchlist_bp, titles_bp]