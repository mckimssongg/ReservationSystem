import requests
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

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

# Ejecución concurrente
with ThreadPoolExecutor() as executor:
    # Realiza 10 reservas de asientos concurrentes
    future_to_seat = {executor.submit(reserve_seat, i, i): i for i in range(1, 11)}
    for future in concurrent.futures.as_completed(future_to_seat):
        seat_number = future_to_seat[future]
        try:
            data = future.result()
        except Exception as exc:
            print(f"La reserva del asiento {seat_number} generó una excepción: {exc}")
        else:
            print(f"Asiento {seat_number} resultó en {data}")

    # Obtener el estado de los asientos después de las reservas
    print("Estado de los asientos después de las reservas:")
    print(get_seats())

    # Realiza 5 cancelaciones de asientos concurrentes
    future_to_seat = {executor.submit(cancel_seat, i, i): i for i in range(1, 6)}
    for future in concurrent.futures.as_completed(future_to_seat):
        seat_number = future_to_seat[future]
        try:
            data = future.result()
        except Exception as exc:
            print(f"La cancelación del asiento {seat_number} generó una excepción: {exc}")
        else:
            print(f"Asiento {seat_number} resultó en {data}")

    # Obtener el estado de los asientos después de las cancelaciones
    print("Estado de los asientos después de las cancelaciones:")
    print(get_seats())
