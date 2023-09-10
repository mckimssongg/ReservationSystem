from threading import Lock
from app.repository.seat_repository import SeatRepository
from app.domain.seat_domain import Seat


class SeatApplication:
    def __init__(self, seat_repository: SeatRepository):
        self.seat_repository = seat_repository
        self.mutex = Lock() # Un mutex para sincronizar las operaciones en hilos múltiples.

    def reserve_seat(self, row: int, seat_number: int) -> str:
        with self.mutex:
            seat = self.seat_repository.load_seat(row, seat_number)  # Cargar el asiento desde la base de datos
            if seat and seat.reserve():  # Utilizar el método del objeto del dominio
                self.seat_repository.save_seat(seat)  # Guardar el estado en la base de datos
                return 'Seat successfully reserved.'
            else:
                return 'Seat is already reserved or invalid.'

    def cancel_seat(self, row: int, seat_number: int) -> str:
        with self.mutex:
            seat = self.seat_repository.load_seat(row, seat_number)  # Cargar el asiento desde la base de datos
            if seat and seat.cancel():  # Utilizar el método del objeto del dominio
                self.seat_repository.save_seat(seat)  # Guardar el estado en la base de datos
                return 'Seat reservation successfully canceled.'
            else:
                return 'Seat is not reserved or invalid.'

    def get_seat_status(self, row: int, seat_number: int) -> str:
        seat = Seat(row, seat_number)
        if self.seat_repository.is_seat_reserved(seat):
            return 'Seat is reserved.'
        elif self.seat_repository.is_seat_available(seat):
            return 'Seat is available.'
        else:
            return 'Seat is invalid.'
        
    def get_all_seats(self):
        return self.seat_repository.get_all_seats()