from flask import Flask
from src.controllers.main_controller import main_blueprint
from src.bot.webhook import bot_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.register_blueprint(main_blueprint)
    app.register_blueprint(bot_blueprint, url_prefix='/webhook')
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)