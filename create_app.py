from flask import Flask
from app.infrastructure.seat_routes import seat_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(seat_routes, url_prefix='/api/seat')
    return app
