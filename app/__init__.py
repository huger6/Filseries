from app.models.models import User
from extensions import app, login_manager
from routes import blueprints


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    # app is already created in extensions.py
    for bp in blueprints:
        app.register_blueprint(bp)

    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login" #redirects to login if user not logged in

    return app

