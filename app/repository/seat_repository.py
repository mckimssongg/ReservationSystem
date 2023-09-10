from sqlite3 import IntegrityError
from app.domain.seat_domain import Seat
from sqlalchemy import create_engine, Column, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class SeatDB(Base):
    __tablename__ = 'seats'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    row = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)
    is_reserved = Column(Boolean, default=False)

class SeatRepository:
    def __init__(self, database_url='sqlite:///seats.db'):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.initialize_seats()

    # Método para verificar si un asiento está reservado
    def is_seat_reserved(self, seat):
        """
        Verifica si un asiento está reservado.
        :param seat: Un objeto de tipo Seat que representa el asiento.
        :return: True si el asiento está reservado, False en caso contrario.
        """
        session = self.Session()
        seat_db = session.query(SeatDB).filter_by(row=seat.row, number=seat.number).first()
        session.close()

        if seat_db and seat_db.is_reserved:
            return True
        return False

    # Método para obtener un asiento específico
    def get_seat(self, row, number):
        """
        Obtiene un asiento específico.
        :param row: Número de fila del asiento.
        :param number: Número del asiento dentro de la fila.
        :return: El objeto del asiento si existe, None en caso contrario.
        """
        session = self.Session()
        seat = session.query(SeatDB).filter_by(row=row, number=number).first()
        session.close()
        return seat

    # Método para reservar un asiento
    def reserve_seat(self, seat=None, row=None, number=None):
        """
        Reserva un asiento.
        :param seat: Objeto del asiento a reservar.
        :param row: Número de fila del asiento a reservar.
        :param number: Número del asiento dentro de la fila a reservar.
        :return: True si el asiento se reserva con éxito, False en caso contrario.
        """
        session = self.Session()
        if seat:
            target_seat = seat
        elif row and number:
            target_seat = self.get_seat(row, number)
        else:
            session.close()
            raise ValueError("Debe proporcionar un objeto 'seat' o 'row' y 'number'.")
        
        if target_seat and not target_seat.is_reserved:
            target_seat.is_reserved = True
            session.commit()
            session.close()
            return True

        session.close()
        return False

    # Método para cancelar la reserva de un asiento
    def cancel_seat(self, seat=None, row=None, number=None):
        """
        Cancela la reserva de un asiento.
        :param seat: Objeto del asiento a cancelar la reserva.
        :param row: Número de fila del asiento a cancelar la reserva.
        :param number: Número del asiento dentro de la fila a cancelar la reserva.
        :return: True si la reserva del asiento se cancela con éxito, False en caso contrario.
        """
        session = self.Session()
        if seat:
            target_seat = seat
        elif row and number:
            target_seat = self.get_seat(row, number)
        else:
            session.close()
            raise ValueError("Debe proporcionar un objeto 'seat' o 'row' y 'number'.")

        if target_seat and target_seat.is_reserved:
            target_seat.is_reserved = False
            session.commit()
            session.close()
            return True

        session.close()
        return False

    # Método para obtener todos los asientos
    def get_all_seats(self):
        """
        Obtiene información de todos los asientos.
        :return: Una lista de diccionarios con información de cada asiento.
        """
        session = self.Session()
        seats = session.query(SeatDB).all()
        session.close()
        return [{"row": seat.row, "number": seat.number, "is_reserved": seat.is_reserved} for seat in seats]

    # Método para verificar si un asiento está disponible
    def is_seat_available(self, seat):
        """
        Verifica si un asiento está disponible para su reserva.
        :param seat: Un objeto de tipo Seat que representa el asiento.
        :return: True si el asiento está disponible, False en caso contrario.
        """
        session = self.Session()
        seat_db = session.query(SeatDB).filter_by(row=seat.row, number=seat.number).first()
        session.close()

        if seat_db and not seat_db.is_reserved:
            return True
        return False
    
    # Método para cargar un asiento desde la base de datos
    def load_seat(self, row, number):
        session = self.Session()
        seat_db = session.query(SeatDB).filter_by(row=row, number=number).first()
        session.close()
        if seat_db:
            seat = Seat(seat_db.row, seat_db.number)
            seat.is_reserved = seat_db.is_reserved
            return seat
        return None

    # Método para guardar un asiento en la base de datos
    def save_seat(self, seat):
        session = self.Session()
        try:
            seat_db = session.query(SeatDB).filter_by(row=seat.row, number=seat.number).first()
            if seat_db:
                session.query(SeatDB).filter_by(row=seat.row, number=seat.number).update({"is_reserved": seat.is_reserved})
                session.commit()
        except Exception as e:
            session.rollback()
        finally:
            session.close()

    def initialize_seats(self):
        """
        Inserta asientos iniciales en la base de datos.
        """
        session = self.Session()

        # Verificar si ya hay asientos en la base de datos
        existing_seats = session.query(SeatDB).first()
        if existing_seats:
            session.close()
            return
        
        # Asientos a insertar
        seats_to_insert = [
            SeatDB(row=1, number=1, is_reserved=False),
            SeatDB(row=1, number=2, is_reserved=False),
            SeatDB(row=1, number=3, is_reserved=False),
            SeatDB(row=1, number=4, is_reserved=False),
            SeatDB(row=1, number=5, is_reserved=False),
            SeatDB(row=2, number=1, is_reserved=False),
            SeatDB(row=2, number=2, is_reserved=False),
            SeatDB(row=2, number=3, is_reserved=False),
            SeatDB(row=2, number=4, is_reserved=False),
            SeatDB(row=2, number=5, is_reserved=False),
            SeatDB(row=3, number=1, is_reserved=False),
            SeatDB(row=3, number=2, is_reserved=False),
            SeatDB(row=3, number=3, is_reserved=False),
            SeatDB(row=3, number=4, is_reserved=False),
            SeatDB(row=3, number=5, is_reserved=False),
            SeatDB(row=4, number=1, is_reserved=False),
            SeatDB(row=4, number=2, is_reserved=False),
            SeatDB(row=4, number=3, is_reserved=False),
            SeatDB(row=4, number=4, is_reserved=False),
            SeatDB(row=4, number=5, is_reserved=False),
            SeatDB(row=5, number=1, is_reserved=False),
            SeatDB(row=5, number=2, is_reserved=False),
            SeatDB(row=5, number=3, is_reserved=False),
            SeatDB(row=5, number=4, is_reserved=False),
            SeatDB(row=5, number=5, is_reserved=False)
        ]
        
        try:
            for seat in seats_to_insert:
                session.add(seat)
            session.commit()
        except IntegrityError:
            session.rollback()
        finally:
            session.close()