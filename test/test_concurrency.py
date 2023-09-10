import requests
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import unittest
import random

# URL del servicio
BASE_URL = "http://localhost:5000/api/seat"

# Función para reservar un asiento
def reserve_seat(row, number):
    response = requests.post(f"{BASE_URL}/reserve", json={"row": row, "number": number})
    return response.json()

# Función para cancelar una reserva de asiento
def cancel_seat(row, number):
    response = requests.post(f"{BASE_URL}/cancel", json={"row": row, "number": number})
    return response.json()

# Función para obtener el estado de todos los asientos
def get_seats():
    response = requests.get(f"{BASE_URL}/seats")
    return response.json()

class TestSeatReservationSystem(unittest.TestCase):

    def setUp(self):
        pass # No es necesario hacer nada

    def test_concurrent_reserve_seat(self):
        with ThreadPoolExecutor() as executor:
            # Realiza 5 reservas de asientos concurrentes aleatorios
            random_seats = [(random.randint(1, 3), random.randint(1, 3)) for _ in range(5)]
            future_to_seat = {executor.submit(reserve_seat, row, number): (row, number) for row, number in random_seats}
            for future in concurrent.futures.as_completed(future_to_seat):
                row, number = future_to_seat[future]
                try:
                    data = future.result()
                    print(f"Asiento (Fila: {row}, Número: {number}) resultó en {data}")
                    print("Estado de los asientos después de la reserva:")
                    print(get_seats())
                except Exception as exc:
                    self.fail(f"La reserva del asiento (Fila: {row}, Número: {number}) generó una excepción: {exc}")

    def test_concurrent_cancel_seat(self):
        with ThreadPoolExecutor() as executor:
            # Primero, reserva algunos asientos aleatorios
            for i in range(3):
                row = random.randint(1, 3)
                number = random.randint(1, 3)
                reserve_seat(row, number)

            # Realiza 5 cancelaciones de asientos concurrentes aleatorios
            random_seats = [(random.randint(1, 3), random.randint(1, 3)) for _ in range(5)]
            future_to_seat = {executor.submit(cancel_seat, row, number): (row, number) for row, number in random_seats}
            for future in concurrent.futures.as_completed(future_to_seat):
                row, number = future_to_seat[future]
                try:
                    data = future.result()
                    print(f"Asiento (Fila: {row}, Número: {number}) resultó en {data}")
                    print("Estado de los asientos después de la cancelación:")
                    print(get_seats())
                except Exception as exc:
                    self.fail(f"La cancelación del asiento (Fila: {row}, Número: {number}) generó una excepción: {exc}")

if __name__ == '__main__':
    unittest.main()
