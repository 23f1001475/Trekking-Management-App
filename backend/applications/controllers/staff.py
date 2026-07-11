
from applications.models import *
from applications.database import db
from flask import url_for
from flask_jwt_extended import get_jwt_identity
from .auth import * 



@app.route("/api/staff/dashboard", methods = ["GET"])  # to get the staff dashboard data
@roles_required('trek_staff')

def staff_dashboard():
    
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    staff_name = user.username

    


    assigned_treks = TrekStaffAssignment.query.filter_by(trek_staff_id = user.id).all()

    assigned_treks_list = []

    for assignment in assigned_treks:

        trek = assignment.trek

        registered_trekkers = Booking.query.filter_by(trek_id = trek.id, booking_status = "Booked").count()

        total_assigned_treks = TrekStaffAssignment.query.filter_by(trek_staff_id = user.id).count()

        total_completed_treks = TrekStaffAssignment.query.filter_by(trek_staff_id = user.id).join(Trek, Trek.id == TrekStaffAssignment.trek_id).filter(Trek.status == "Completed").count()

        

        trek_data = {

            "trek_id": trek.id,
            "route_name": trek.route.route_name,
            "status": trek.status,
            "start_date": trek.start_date.isoformat(),
            "end_date": trek.end_date.isoformat() ,
            "registered_trekkers": registered_trekkers,
        }

        assigned_treks_list.append(trek_data)

    return jsonify(staff_name = staff_name, assigned_treks = assigned_treks_list, total_assigned_treks = total_assigned_treks, total_completed_treks = total_completed_treks), 200






@app.route("/api/staff/treks/<int:trek_id>", methods = ["GET"]) #to get the specific staff trek assigned to them

@roles_required('trek_staff')

def get_assigned_trek(trek_id):

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    trek_assignment = TrekStaffAssignment.query.filter_by(trek_id = trek_id, trek_staff_id = user.id).first()


    if not trek_assignment:
        return jsonify({"msg": "Trek not found or not assigned to you"}), 404
    
    trek = trek_assignment.trek

    registered_trekkers = Booking.query.filter_by(trek_id = trek.id, booking_status = "Booked").count()


    assigned_staffs = []
    for assignment in trek.trek_staff_assignment:

        trek_staff = assignment.staff

        assigned_staffs.append(trek_staff.username)

    
    
    trek_data = {
        "trek_id": trek.id,
        "route_name": trek.route.route_name,
        "status": trek.status,
        "start_date": trek.start_date.isoformat(),
        "end_date": trek.end_date.isoformat(),
        "location" : trek.route.location,
        "description" : trek.route.description,
        "difficulty" : trek.route.difficulty,
        "altitude" : trek.route.altitude,
        "days_on_trail" : trek.route.days_on_trail,
        "total_slots" : trek.total_slots,
        "available_slots" : trek.available_slots,
        "image" : url_for('static', filename = trek.route.image, _external = True), #trek.route.image  image stored path is like  trek_images/Screenshot_1.png
        "registered_trekkers": registered_trekkers,

        "assigned_staffs" : assigned_staffs
    }
    

    return jsonify(trek_data), 200






@app.route("/api/staff/treks/<int:trek_id>/participants", methods = ["GET"]) #to get the participants of the specific trek assigned to the staff

@roles_required('trek_staff')

def get_participants(trek_id):

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    trek_assignment  = TrekStaffAssignment.query.filter_by(trek_id = trek_id, trek_staff_id = user.id).first()

    

    if not trek_assignment:
        return jsonify({"msg": "Trek not found or not assigned to you"}), 404
    
    trek = trek_assignment.trek

    trek_name = trek.trek_name

    participants = Booking.query.filter_by(trek_id = trek.id, booking_status = "Booked").all()

    participants_list = []

    for participant in participants:

        participant_data = {
            "booking_id": participant.id,
            "trekker_id": participant.user_id,
            "name": participant.trekker.username,
            "email": participant.trekker.email,
            "phone": participant.trekker.phone,
        }

        participants_list.append(participant_data)

    return jsonify(participants_list = participants_list, trek_name = trek_name), 200








@app.route("/api/staff/trek_update/<int:trek_id>/slots", methods = ["POST"]) # to update the slots and status of the trek assigned to the staff

@roles_required('trek_staff')
def update_trek_slots(trek_id):

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    trek_assignment = TrekStaffAssignment.query.filter_by(trek_id = trek_id, trek_staff_id = user.id).first()

    if not trek_assignment:
        return jsonify({"msg": "Trek not found or not assigned to you"}), 404
    
    trek = trek_assignment.trek

    trek.available_slots = request.json.get('available_slots')
    trek.status = request.json.get('status', trek.status)  # if status is not provided, keep the current status
 

    db.session.commit()

    return jsonify({"msg": "Trek slots updated successfully"}), 200


