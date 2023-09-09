from threading import Lock
from app.repository.seat_repository import SeatRepository
from app.domain.seat_domain import Seat


class SeatApplication:
    def __init__(self, seat_repository: SeatRepository):
        self.seat_repository = seat_repository
        self.mutex = Lock()

    def reserve_seat(self, row: int, seat_number: int) -> str:
        with self.mutex:
            seat = Seat(row, seat_number)
            if self.seat_repository.is_seat_available(seat):
                self.seat_repository.reserve_seat(seat)
                return 'Seat successfully reserved.'
            else:
                return 'Seat is already reserved or invalid.'

    def cancel_seat(self, row: int, seat_number: int) -> str:
        with self.mutex:
            seat = Seat(row, seat_number)
            if self.seat_repository.is_seat_reserved(seat):
                self.seat_repository.cancel_seat(seat)
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