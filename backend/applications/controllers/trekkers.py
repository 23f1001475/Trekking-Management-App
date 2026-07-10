from flask import jsonify, request, current_app as app, url_for
from applications.models import *
from .auth import *
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from werkzeug.security import generate_password_hash
from datetime import datetime



# User dashboard: Available treks, Booked treks, Trek status

@app.route('/api/trekkers/dashboard', methods = ["GET"])
@roles_required('trekker')
def user_dashboard():

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    trekker_name = user.username

    available_treks = Trek.query.filter_by(status = "Open").count()

    booked_treks = Booking.query.filter_by(user_id = user.id, booking_status = "Booked").count()


    available = Trek.query.filter_by(status = "Open").all()

    available_list = []

    for trek in available:

        trek_data = {
            "trek_id": trek.id,
            "trek_name": trek.trek_name,
            "status": trek.status,
            "start_date": trek.start_date.isoformat(),
            "end_date": trek.end_date.isoformat(),
            "available_slots": trek.available_slots,
            "price": trek.price,
            "difficulty" : trek.route.difficulty
        }

        available_list.append(trek_data)


    # Booked treks for current user
    bookings = Booking.query.filter_by(user_id = user.id).order_by(Booking.booking_date.desc()).all()
    booked_list = []

    for booking in bookings:
        booking_data = {
            "booking_id": booking.id,
            "trek_id": booking.trek.id,
            "trek_name": booking.trek.route.route_name,
            "booking_date": booking.booking_date.isoformat(),
            "start_date": booking.trek.start_date.isoformat(),
            "end_date": booking.trek.end_date.isoformat(),
            
            "status": booking.booking_status,
            "difficulty" : booking.trek.route.difficulty
        }

        booked_list.append(booking_data)

    return jsonify(available_treks = available_list, booked_treks = booked_list, trekker_name = trekker_name, available_treks_count = available_treks, booked_treks_count = booked_treks,  user_id = user.id,  role = user.role), 200







# Get trek (for booking form)

@app.route('/api/trekkers/treks/<int:trekID>', methods=["GET"])    # for viewing all treks
@roles_required('trekker')
def get_trek(trekID):

    trek = Trek.query.get(trekID)



    trek_data = {

            "trek_id": trek.id,
            "trek_name": trek.trek_name,
            "description" : trek.route.description,
            "location"  : trek.route.location,
            "start_date": trek.start_date.isoformat(),
            "end_date" : trek.end_date.isoformat(),
            "difficulty" : trek.route.difficulty,
            "altitude" : trek.route.altitude,
            "price": trek.price,
            "available_slots": trek.available_slots,
            "status": trek.status,
            "image" : url_for('static', filename = trek.route.image, _external = True), #trek.route.image  image stored path is like  trek_images/Screenshot_1.png
        }
    

    return jsonify(trek = trek_data), 200









# Book a trek

@app.route('/api/trekkers/bookings', methods=["POST"])   # to show the booking form and book the trek
@roles_required("trekker")
def book_trek():

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    trek_id = request.json.get("trek_id")

    if not trek_id:
        return jsonify({"msg": "trek_id is required"}), 400

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"msg": "Trek not found"}), 404
 

    if trek.status != "Open":
        return jsonify({"msg": "This trek is not open for booking"}), 400

    if trek.available_slots <= 0:
        return jsonify({"msg": "No slots available"}), 400

    # Prevent duplicate booking
    existing_booking = Booking.query.filter_by( trek_id=trek.id , user_id=user.id, booking_status = "Booked").first()

    if existing_booking:
        return jsonify({"msg": "You have already booked this trek"}), 400

    booking = Booking(
        trek_id = trek.id,
        user_id = user.id,
        booking_status = "Booked",
        booking_date = datetime.utcnow(),
        total_amount = trek.price,
    )


    db.session.add(booking)

    trek.available_slots -= 1    #one slot booked


    if trek.available_slots == 0:
        trek.status = "Closed"

    db.session.commit()

    
    return jsonify({"msg": "Booking created",  "booking_id": booking.id, "trek_id": trek.id, "available_slots" : trek.available_slots}), 201








# cancel a trek booking
@app.route('/api/trekkers/bookings/<int:booking_id>/cancel', methods = ["POST"])
@roles_required('trekker')

def cancel_booking(booking_id):

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    booking = Booking.query.filter_by(id = booking_id, user_id = user.id).first()

    if not booking:
        return jsonify({"msg": "Booking not found"}), 404

    trek = booking.trek

    if not trek:
        return jsonify({"msg": "Trek not found"}), 404

    booking.booking_status = "Cancelled"
    trek.available_slots += booking.participants or 1    #one slot cancelled so increae by one and participants will define the no. of slots cancelled (although in this applicaiton i have set it to 1 (only one participant can book i tso it is bydefault 1))

    if trek.status == "Closed" and trek.available_slots > 0:
        trek.status = "Open"

    db.session.commit()
    
    return jsonify({"msg": "Booking cancelled"}), 200








@app.route('/api/trekkers/bookings', methods=["GET"])   # to show all bookings for the current user
@roles_required('trekker')

def get_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    
    data = []
    for booking in bookings:
        booking_data = {
            "booking_id" : booking.id,
            "trek_id" : booking.trek.id,
            "trek_name" : booking.trek.route.route_name,
            "booking_date" : booking.booking_date.isoformat(),
            "status" : booking.booking_status
        }

        data.append(booking_data)

    return jsonify(bookings = data), 200









# Get booking detail / status of current booking

@app.route('/api/trekkers/bookings/<int:booking_id>', methods=["GET"])
@roles_required('trekker')

def get_booking_detail(booking_id):

    booking = Booking.query.filter_by(id = booking_id, user_id = current_user.id).first()

    if not booking:
        return jsonify({"msg": "Booking not found"}), 404

    data = {
        "booking_id": booking.id,
        "trek_id": booking.trek.id,
        "trek_name": booking.trek.route.route_name if booking.trek.route else None,
        "booking_date": booking.booking_date.isoformat() if booking.booking_date else None,
        "status": booking.booking_status,
        "participants": booking.participants
    }
    return jsonify(booking = data), 200







# Trekking history (past bookings)

@app.route('/api/trekkers/history', methods=["GET"])
@roles_required('trekker')
def trekking_history():

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    bookings = Booking.query.filter_by(user_id = user.id).order_by(Booking.booking_date.desc()).all()
    

    history_data = []

    for booking in bookings:
        if booking.booking_status in ['Booked', 'Cancelled']:

            history = {

                "booking_id": booking.id,
                "trek_id": booking.trek.id,
                "trek_name": booking.trek.route.route_name,
                "booking_date": booking.booking_date.isoformat(),
                "end_date" : booking.trek.end_date.isoformat(),
                "price" : booking.total_amount,
                "status": booking.booking_status,
                "trek_status" : booking.trek.status   #if trek_status = closed then trek is completed
            }
            
            history_data.append(history)

    return jsonify(history_data = history_data), 200








# this is to Get or edit user profile
@app.route('/api/trekkers/profile', methods=["GET", "PUT"])
@roles_required('trekker')

def user_profile():

    user_id = get_jwt_identity()
    # user = User.query.get(user_id)
    u = User.query.get(user_id)

    if not u:
            return jsonify({"msg": "User not found"}), 400

    if request.method == 'GET':

        return jsonify(

            id = u.id,
            username = u.username,
            email = u.email,
            phone = u.phone,

        ), 200
    


    # PUT - update profile

    user_data = request.json or {}

    username = user_data.get('username')
    email = user_data.get('email')
    phone = user_data.get('phone')

    # check uniqueness



    if username and User.query.filter(User.username == username, User.id != u.id).first():
        return jsonify({"msg": "username already exists"}), 400
    
    if email and User.query.filter(User.email == email, User.id != u.id).first():
        return jsonify({"msg": "email already exists"}), 400
    
    if phone and User.query.filter(User.phone == phone, User.id != u.id).first():
        return jsonify({"msg": "phone number already exists"}), 400


    if username:
        u.username = username

    if email:
        u.email = email
    if phone:
        u.phone = phone

    db.session.commit()

    return jsonify({"msg": "Profile updated"}), 200
    


