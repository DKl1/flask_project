from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as enum

engine = create_engine("mysql+pymysql://root:yevhe@localhost:3306/hotel", echo=True)

base = declarative_base()

class Type(enum):
    economy = 'economy'
    comfort = 'comfort'
    comfortplus = 'comfort+'
    luxe = 'luxe'

class Admin(base):
    __tablename__ = 'admin'

    admin_id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable = False)
    username = Column(String, nullable = False)
    password = Column(String, nullable = False)

    def __init__(self, admin_id, full_name, username, password):
        self.admin_id = admin_id
        self.full_name = full_name
        self.username = username
        self.password = password

class Room(base):
    __tablename__ = 'room'

    room_number = Column(String, primary_key=True)
    people = Column(Integer, nullable = False)
    type = Column(Enum(Type), nullable = False)
    price = Column(Integer, nullable = False)
    reserved = Column(Boolean, ForeignKey('reserved.status'), nullable = False)
    description = Column(String, nullable = False)
    photo = Column(String, nullable = True)
    beds = Column(Integer, nullable = True)

    def __init__(self, room_number, people, type, price, reserved, description, photo, beds):
        self.room_number = room_number
        self.people = people
        self.type = type
        self.price = price
        self.reserved = reserved
        self.description = description
        self.photo = photo
        self.beds = beds

class Reservation(base):
    __tablename__ = 'reservation'
    
    reservation_id = Column(Integer, primary_key = True)
    full_name = Column(String, nullable = False)
    phone = Column(String, nullable = False)
    date_from = Column(String, nullable = False)
    date_to = Column(String, nullable = False)

    def __init__(self, reservation_id, full_name, phone, date_from, date_to):
        self.reservation_id = reservation_id
        self.full_name = full_name
        self.phone = phone
        self.date_from = date_from
        self.date_to = date_to

class Reserved(base):
    __tablename__ = 'reserved'

    status = Column(Boolean, nullable = False)
    room_number = Column(String, ForeignKey('room.room_number'), nullable = False)
    date_from = Column(String, ForeignKey('reservation.date_from'), nullable = False)
    date_to = Column(String, ForeignKey('reservation.date_to'), nullable = False)

    def __init__(self, status, room_number, date_from, date_to):
        self.status = status
        self.room_number = room_number
        self.date_from = date_from
        self.date_to = date_to