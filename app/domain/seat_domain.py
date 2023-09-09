from threading import Lock

# Domain Model for Seat Reservation

class Seat:
    def __init__(self, row, number):
        self.row = row
        self.number = number
        self.is_reserved = False
        self.lock = Lock()

    def reserve(self):
        with self.lock:
            if not self.is_reserved:
                self.is_reserved = True
                return True
            return False

    def cancel(self):
        with self.lock:
            if self.is_reserved:
                self.is_reserved = False
                return True
            return False