
from applications.models import *
from applications.database import db
from .auth import * 



@app.route("/api/admin/dashboard", methods = ["GET"])  # to get the staff dashboard data
@roles_required('staff')

def staff_dashboard():
    
    staff_name = current_user.username

    assigned_treks = Trek.query.filter_by(staff_id = current_user.id).all()

    assigned_treks_list = []

    for trek in assigned_treks:

        registered_trekkers = Booking.query.filter_by(trek_id = trek.id).count()

        trek_data = {
            "trek_id": trek.id,
            "route_name": trek.route.route_name,
            "status": trek.status,
            "start_date": trek.start_date.isoformat(),
            "end_date": trek.end_date.isoformat() if trek.end_date else None,
            "registered_trekkers": registered_trekkers,
        }

        assigned_treks_list.append(trek_data)

    return jsonify(staff_name = staff_name, assigned_treks = assigned_treks_list), 200






@app.route("/api/staff/treks/<int:trek_id>", methods = ["GET"]) #to get the specific staff trek assigned to them

@roles_required('staff')

def get_assigned_trek(trek_id):

    trek = Trek.query.filter_by(id = trek_id, staff_id = current_user.id).first()

    if not trek:
        return jsonify({"msg": "Trek not found or not assigned to you"}), 404

    registered_trekkers = Booking.query.filter_by(trek_id = trek.id).count()

    trek_data = {
        "trek_id": trek.id,
        "route_name": trek.route.route_name,
        "status": trek.status,
        "start_date": trek.start_date.isoformat(),
        "end_date": trek.end_date.isoformat() if trek.end_date else None,
        "registered_trekkers": registered_trekkers,
    }

    return jsonify(trek_data), 200






@app.route("/api/staff/treks/<int:trek_id>/participants", methods = ["GET"]) #to get the participants of the specific trek assigned to the staff

@roles_required('staff')

def get_participants(trek_id):

    trek = Trek.query.filter_by(id = trek_id, staff_id = current_user.id).first()

    if not trek:
        return jsonify({"msg": "Trek not found or not assigned to you"}), 404

    participants = Booking.query.filter_by(trek_id = trek.id).all()

    participants_list = []

    for participant in participants:

        participant_data = {
            "booking_id": participant.id,
            "trekker_id": participant.trekker_id,
            "name": participant.trekker.name,
            "email": participant.trekker.email,
            "phone": participant.trekker.phone,
        }

        participants_list.append(participant_data)

    return jsonify(participants = participants_list), 200








@app.route("/api/staff/trek_update/<int:trek_id>/slots", methods = ["POST"]) # to update the slots of the trek assigned to the staff

@roles_required('staff')
def update_trek_slots(trek_id):

    trek = Trek.query.filter_by(id = trek_id, staff_id = current_user.id).first()

    if not trek:
        return jsonify({"msg": "Trek not found or not assigned to you"}), 404

    trek.available_slots = request.json.get('available_slots')
    trek.status = request.json.get('status', trek.status)  # if status is not provided, keep the current status
 

    db.session.commit()

    return jsonify({"msg": "Trek slots updated successfully"}), 200


