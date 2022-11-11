from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as enum

engine = create_engine("mysql+pymysql://root:rootadmin2022@localhost:3306/hotel", echo=True)

base = declarative_base()

class Type(enum):
    economy = 'economy'
    comfort = 'comfort'
    comfortplus = 'comfort+'
    luxe = 'luxe'

class Admin(base):
    __tablename__ = 'admin'

    admin_id = Column("admin_id", Integer, primary_key=True)
    full_name = Column("full_name", String(50), nullable = False)
    username = Column("username",String(40), nullable = False)
    password = Column("password", String(225), nullable = False)

    def __init__(self, full_name, username, password):
        self.full_name = full_name
        self.username = username
        self.password = password

class Room(base):
    __tablename__ = 'room'

    room_number = Column("room_number", String(3), primary_key=True)
    people = Column("people", Integer, nullable = False)
    type = Column("type", Enum(Type), nullable = False)
    price = Column("price", Integer, nullable = False)
    description = Column("description", String(300), nullable = False)
    photo_url = Column("photo_url", String(120), nullable = True)
    bed_n = Column("bed_n", Integer, nullable = True)

    def __init__(self, room_number, people, type, price, description, photo_url, bed_n):
        self.room_number = room_number
        self.people = people
        self.type = type
        self.price = price
        self.description = description
        self.photo_url = photo_url
        self.bed_n = bed_n

class Reservation(base):
    __tablename__ = 'reservation'

    reservation_id = Column(Integer, primary_key=True)
    full_name = Column(String(50), nullable=False)
    phone = Column(String(13), nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    id_room = Column(String(3), ForeignKey(Room.room_number), nullable=False)

    def __init__(self, full_name, phone, date_from, date_to):
        self.full_name = full_name
        self.phone = phone
        self.date_from = date_from
        self.date_to = date_to


if __name__ == "__main__":
    base.metadata.drop_all(bind=engine)