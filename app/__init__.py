from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Registrar blueprints
    from app.routes import main, referencias, ordenes, procesos, inventario

    app.register_blueprint(main.bp)
    app.register_blueprint(referencias.bp)
    app.register_blueprint(ordenes.bp)
    app.register_blueprint(procesos.bp)
    app.register_blueprint(inventario.bp)

    with app.app_context():
        db.create_all()

    return app
