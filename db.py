from sqlalchemy import *
from enum import Enum as enum
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, scoped_session

from marshmallow_sqlalchemy import *
from marshmallow import fields, validate, ValidationError


engine = create_engine("mysql+pymysql://root:Klym305@localhost:3306/hotel_db", echo=True)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
base = declarative_base()
base.metadata.create_all(bind=engine)


def validate_entry_id(entry, room_number):
    if Session.query(entry).filter(entry.room_number == room_number).count() == 0:
        return False
    return True


def validate_phone(phone_number):
    temp = 0
    for i in phone_number:
        if i.isalpha():
            temp += 1
    if temp > 0 or len(phone_number) < 1 or len(phone_number) > 13:
        return False
    return True


class Type(enum):
    economy = 'economy'
    comfort = 'comfort'
    comfortplus = 'comfort+'
    luxe = 'luxe'


class Admin(base):
    __tablename__ = 'admin'

    admin_id = Column("admin_id", Integer, primary_key=True)
    full_name = Column("full_name", String(50), nullable=False)
    username = Column("username", String(40), nullable=False)
    password = Column("password", String(225), nullable=False)

    def __init__(self, admin_id,
                 full_name, username, password):
        self.admin_id = admin_id
        self.full_name = full_name
        self.username = username
        self.password = password


class Room(base):
    __tablename__ = 'room'

    room_number = Column("room_number", String(3), primary_key=True)
    people = Column("people", Integer, nullable=False)
    type = Column("type", Enum(Type), nullable=False)
    price = Column("price", Integer, nullable=False)
    description = Column("description", String(300), nullable=False)
    photo_url = Column("photo_url", String(120), nullable=True)
    bed_n = Column("bed_n", Integer, nullable=True)

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

    def __init__(self, reservation_id, full_name, phone, date_from, date_to, id_room):
        self.reservation_id = reservation_id
        self.full_name = full_name
        self.phone = phone
        self.date_from = date_from
        self.date_to = date_to
        self.id_room = id_room


class RoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        include_relationships = False
        load_instance = True
        include_fk = True

    room_number = fields.Integer(validate=validate.Range(1, 200))
    people = fields.Integer(validate=validate.Range(1, 30))
    type = fields.String(validate=validate.OneOf(["economy", "comfort", "comfort+", "luxe"]), required=True)
    price = fields.Integer(validate=validate.Range(1, 1000000))
    description = fields.String(validate=validate.Length(min=10, max=300))
    photo_url = fields.String(validate=validate.Length(min=10, max=120))
    bed_n = fields.Integer(validate=validate.Range(1, 15))


class ReservationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Reservation
        include_relationships = False
        load_instance = True
        include_fk = True

    reservation_id = fields.Integer(validate=validate.Range(1, 200))
    full_name = fields.String(validate=validate.Length(min=10, max=50))
    phone = fields.String(validate=validate_phone)
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    id_room = fields.Integer(validate=validate.Range(1, 200))


class AdminSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Admin
        include_relationships = False
        load_instance = True
        include_fk = True

    full_name = fields.String(validate=validate.Length(min=10, max=50))
    username = fields.String(validate=validate.Length(min=10, max=50))
    password = fields.String(validate=validate.Length(min=10, max=30))


