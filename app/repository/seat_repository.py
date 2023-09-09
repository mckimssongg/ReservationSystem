from app.domain.seat_domain import Seat
from sqlalchemy import create_engine, Column, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class SeatDB(Base):
    __tablename__ = 'seats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    row = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)
    is_reserved = Column(Boolean, default=False)

class SeatRepository:
    def __init__(self, database_url='sqlite:///seats.db'):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_seat(self, row, number):
        session = self.Session()
        seat = session.query(SeatDB).filter_by(row=row, number=number).first()
        session.close()
        return seat

    def reserve_seat(self, row, number):
        session = self.Session()
        seat = self.get_seat(row, number)
        if seat and not seat.is_reserved:
            seat.is_reserved = True
            session.commit()
            session.close()
            return True
        session.close()
        return False

    def cancel_seat(self, row, number):
        session = self.Session()
        seat = self.get_seat(row, number)
        if seat and seat.is_reserved:
            seat.is_reserved = False
            session.commit()
            session.close()
            return True
        session.close()
        return 
    
    def get_all_seats(self):
        session = self.Session()
        seats = session.query(SeatDB).all()
        session.close()
        return [{"row": seat.row, "number": seat.number, "is_reserved": seat.is_reserved} for seat in seats]
