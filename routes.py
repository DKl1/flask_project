from flask import current_app as application
from flask import request, Flask
from flask_bcrypt import generate_password_hash, check_password_hash
from db import *
import json
from main import app


@app.route('/rooms/', methods=['GET'])
def get_room_by_number():
    session = Session()
    args = request.args
    room_number = args.get('room_number')
    room = session.query(Room).filter(Room.room_number == room_number).first()
    room_schema = RoomSchema()
    res = room_schema.dump(room)
    session.close()
    return res, 200


@app.route('/rooms/', methods=['PUT'])
def update_room():
    session = Session()
    args = request.get_json()
    arg = request.args
    room_number = arg.get('room_number')
    room_schema = RoomSchema()
    try:
        room = room_schema.load(args, session=session)
        session.query(Room).filter(Room.room_number == room_number).update(args)
        session.commit()
        room = room_schema.dump(session.query(Room).filter(Room.room_number == room_number).first())
        session.commit()
        session.close()
        return room, 200
    except ValidationError as error:
        session.close()
        return str(error), 400


#
#
# @app.route('/rooms/', methods=['DELETE'])
# def delete_room():
#     session = Session()
#     args = request.args
#     room_number = int(args.get('room_number'))
#     # if session.query(Room).filter(Room.room_number == room_number).count() == 0:
#     #     session.close()
#     #     return "Such room doesn't exist", 404
#     room = session.query(Room).filter(Room.room_number == room_number)
#     session.query(Room).filter(Room.room_number == room_number).delete()
#     session.query(Reservation).filter(Reservation.id_room == room_number).delete()
#     session.commit()
#     session.close()
#     return room, 200
@app.route('/rooms/<int:room_number>', methods=['DELETE'])
def delete_user(room_number):
    # args = request.args
    # tour_id = args.get('tour_id')
    if validate_entry_id(Room, room_number):
        # return {"message": "Tour with such id does not exist"}, 400
        session = Session()
        session.query(Reservation).filter(Reservation.id_room == room_number).delete()
        session.query(Room).filter(Room.room_number == room_number).delete()

        session.commit()
        session.close()
        return {"message": "Room deleted successfully"}, 200
    return {"message": "Room with such id does not exist"}, 404


@app.route('/rooms', methods=['GET'])
def get_rooms():
    session = Session()
    rooms = session.query(Room)
    room_schema = RoomSchema()
    res = json.dumps([room_schema.dump(i) for i in rooms])
    session.close()
    return res, 200


#
#
@app.route('/rooms', methods=['POST'])
def post_room():
    session = Session()
    args = request.get_json()
    try:
        room_schema = RoomSchema()
        room = room_schema.load(args, session=session)
        session.add(room)
        session.commit()
        res = room_schema.dump(room)
        session.close()
        return res, 200
    except ValidationError as error:
        session.close()
        return str(error), 400


@app.route('/rooms/reserve/', methods=['POST'])
def add_reserve():
    session = Session()
    args = request.get_json()
    try:
        reservation_schema = ReservationSchema()
        reservation = reservation_schema.load(args, session=session)
        session.add(reservation)
        session.commit()
        res = reservation_schema.dump(reservation)
        session.close()
        return res, 200
    except ValidationError as error:
        session.close()
        return str(error), 400


@app.route('/rooms/reserve/', methods=['GET'])
def get_reserve():
    session = Session()
    reservations = session.query(Reservation)
    reservation_schema = ReservationSchema()
    res = json.dumps([reservation_schema.dump(i) for i in reservations])
    session.close()
    return res, 200


@app.route('/admin', methods=['POST'])
def post_admin():
    session = Session()
    args = request.get_json()
    try:
        admin_schema = AdminSchema()
        admin = admin_schema.load(args, session=session)
        if session.query(Admin).filter(Admin.username == admin.username).count() != 0:
            return {"message": "Username already exists"}, 422
        admin.password = generate_password_hash(admin.password)
        session.add(admin)
        session.commit()
        res = admin_schema.dump(admin)
        session.close()
        return res, 200
    except ValidationError as error:
        session.close()
        return str(error), 400


@app.route('/admin', methods=['GET'])
def get_admin():
    session = Session()
    args = request.args
    admin_id = args.get('admin_id')
    admin = session.query(Admin).filter(Admin.admin_id == admin_id).first()
    admin_schema = AdminSchema()
    res = admin_schema.dump(admin)
    session.close()
    return res, 200

# # @app.route('/rooms/reserve/', methods=['DELETE'])
# def delete_reserve():
#     pass
