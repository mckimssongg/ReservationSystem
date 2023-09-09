from flask import Blueprint, jsonify, request
from app.application.seat_application import SeatApplication
from app.domain.seat_domain import Seat
from app.repository.seat_repository import SeatRepository
from ..utils.logger import LoggerConfig, log_decorator

# Crear un Blueprint
seat_routes = Blueprint('seat_routes', __name__)

# Configuración de logger
logger = LoggerConfig("SeatReservation")

# Repositorio y aplicación de asientos
seat_repository = SeatRepository()
seat_application = SeatApplication(seat_repository)

@seat_routes.route('/seats', methods=['GET'])
@log_decorator(logger, level="info")
def get_seats():
    seats = seat_application.get_all_seats()
    return jsonify(seats), 200

@seat_routes.route('/reserve', methods=['POST'])
@log_decorator(logger, level="info")
def reserve_seat():
    data = request.json
    result = seat_application.reserve_seat(data['row'], data['number'])
    return jsonify({'message': result}), 200

@seat_routes.route('/cancel', methods=['POST'])
@log_decorator(logger, level="info")
def cancel_seat():
    data = request.json
    result = seat_application.cancel_seat(data['row'], data['number'])
    return jsonify({'message': result}), 200
