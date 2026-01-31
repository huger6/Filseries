from flask_login import current_user
from app.models import User
from app.extensions import app, login_manager, db
from app.routes import blueprints
from app.utils.converters import MediaTypeConverter
from app.services.db_info import get_user_pfp


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_user_pfp():
    """Make has_pfp available in all templates"""
    if current_user.is_authenticated:
        return {'has_pfp': get_user_pfp(current_user.id) is not None}
    return {'has_pfp': False}

def create_app():
    # app is already created in extensions.py

    # Register converter
    app.url_map.converters["media"] = MediaTypeConverter

    # Register all blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # redirects to login if user not logged in

    return app

