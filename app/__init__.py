from app.models import User
from app.extensions import app, login_manager, db
from app.routes import blueprints
from app.utils.converters import MediaTypeConverter


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

