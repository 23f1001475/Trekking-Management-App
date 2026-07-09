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

    booked_treks = Booking.query.filter_by(user_id = user.id).count()


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

    trek_data = {

            "trek_id": trek.id,
            "trek_name": trek.route.route_name,
            "status": trek.status,
            "start_date": trek.start_date.isoformat(),
            "end_date" : trek.end_date.isoformat(),
            "difficulty" : trek.route.difficulty,
            "price": trek.price,
            "description" : trek.route.description, 
        }

    

    if trek.status != "Open":
        return jsonify({"msg": "This trek is not open for booking"}), 400

    if trek.available_slots <= 0:
        return jsonify({"msg": "No slots available"}), 400

    # Prevent duplicate booking
    existing_booking = Booking.query.filter_by( trek_id=trek.id , user_id=user.id).first()

    if existing_booking:
        return jsonify({"msg": "You have already booked this trek"}), 400

    booking = Booking(
        trek_id=trek.id,
        user_id=user.id,
        booking_status="Booked",
        booking_date=datetime.utcnow(),
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

    # Return all bookings for now; front-end can filter by status if needed
    bookings = Booking.query.filter_by(user_id = current_user.id).order_by(Booking.booking_date.desc()).all()
    
    for booking in bookings:
        if booking.booking_status in ['Booked', 'Cancelled']:
            history_data = {
                "booking_id": booking.id,
                "trek_id": booking.trek.id,
                "trek_name": booking.trek.route.route_name if booking.trek.route else None,
                "booking_date": booking.booking_date.isoformat() if booking.booking_date else None,
                "status": booking.booking_status
            }
            
            history_data.append(history_data)

    return jsonify(history=[history_data]), 200








# Get or edit user profile
@app.route('/api/trekkers/profile', methods=["GET", "PUT"])
@roles_required('trekker')
def user_profile():
    if request.method == 'GET':
        u = current_user
        return jsonify(
            id=u.id,
            username=u.username,
            email=u.email,
            phone=u.phone,
            role=u.role
        ), 200

    # PUT - update profile

    data = request.json or {}
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')

    # check uniqueness

    if username and User.query.filter(User.username == username, User.id != current_user.id).first():
        return jsonify({"msg": "username already exists"}), 400
    
    if email and User.query.filter(User.email == email, User.id != current_user.id).first():
        return jsonify({"msg": "email already exists"}), 400
    
    if phone and User.query.filter(User.phone == phone, User.id != current_user.id).first():
        return jsonify({"msg": "phone number already exists"}), 400

    try:
        if username:
            current_user.username = username
        if email:
            current_user.email = email
        if phone:
            current_user.phone = phone

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Could not update profile", "error": str(e)}), 500

    return jsonify({"msg": "Profile updated"}), 200


# # Search treks by query param 'q' (route name or other text)
# @app.route('/api/trekkers/treks/search', methods=["GET"])
# def search_treks():
#     q = request.args.get('q', '').strip()
#     status = request.args.get('status')

#     treks = Trek.query.all()
#     results = []
#     for t in treks:
#         route_name = getattr(getattr(t, 'route', None), 'route_name', '') or ''
#         trek_name = getattr(t, 'name', '') or ''
#         if q:
#             if q.lower() in route_name.lower() or q.lower() in trek_name.lower():
#                 pass
#             else:
#                 continue
#         if status and getattr(t, 'status', None) != status:
#             continue
#         results.append({
#             "trek_id": t.id,
#             "route_name": route_name,
#             "trek_name": trek_name,
#             "status": getattr(t, 'status', None),
#             "start_date": getattr(t, 'start_date', None).isoformat() if getattr(t, 'start_date', None) else None
#         })

#     return jsonify(results=results), 200
