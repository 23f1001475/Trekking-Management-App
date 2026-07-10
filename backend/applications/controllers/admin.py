from .auth import *
from applications.models import *   

from flask_jwt_extended import get_jwt_identity


@app.route('/api/admin/dashboard', methods = ["GET"])
@roles_required('admin')

def admin_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    Admin_name = user.username
    total_treks = TrekRoute.query.count()
    active_treks = Trek.query.filter_by(status = "Open").count()
    total_bookings = Booking.query.count()
    total_staff = User.query.filter_by(role = "trek_staff", is_active = True, is_deleted = False).count()
    total_trekkers = User.query.filter_by(role = "trekker", is_active = True, is_deleted = False).count()

    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).all()

    result_recent_bookings = []

    for booking in recent_bookings:
        booking_data = {
            "trek_name" : booking.trek.trek_name,   
            "trekker": booking.trekker.username,
            "trek_name": booking.trek.route.route_name,
            "booking_date": booking.booking_date.isoformat(),
            "start_date": booking.trek.start_date.isoformat(),
            "end_date": booking.trek.end_date.isoformat(),
            "booking_status": booking.booking_status,
            "trek_status": booking.trek.status
        }
        result_recent_bookings.append(booking_data)

    recent_treks = Trek.query.order_by(Trek.created_at.desc()).all()

    result_recent_treks = []

    for trek in recent_treks:
        trek_data = {

            "trek_name": trek.trek_name,
            "location": trek.route.location,
            "duration" : trek.route.days_on_trail,
            "difficulty": trek.route.difficulty,
            "price" : trek.price,
            "altitude" : trek.route.altitude,
            "status": trek.status

        }
        result_recent_treks.append(trek_data)

    return jsonify(
        Admin_name = Admin_name, total_treks = total_treks,
        active_treks = active_treks, total_bookings = total_bookings,
        total_staff = total_staff, total_trekkers = total_trekkers,
        recent_bookings = result_recent_bookings, recent_treks = result_recent_treks
    ), 200






    
@app.route('/api/admin/create_trek_route', methods = ["POST"])  # to create new trek route
@roles_required('admin')

def create_trek_route():

    trek_route_data = request.form


    errors = {}

    route_name = trek_route_data.get("route_name")
    location = trek_route_data.get("location")
    difficulty = trek_route_data.get("difficulty")
    days_on_trail = trek_route_data.get("days_on_trail")
    description = trek_route_data.get("description")
    altitude = trek_route_data.get("altitude")
    image = request.files.get("image")

    if "route_name" not in errors:
        errors["route_name"] = []

    if "location" not in errors:
        errors["location"] = []

    if "difficulty" not in errors:
        errors["difficulty"] = []
    
    if "altitude" not in errors:
        errors["altitude"] = []

    if "days_on_trail" not in errors:
        errors["days_on_trail"] = []

    if "description" not in errors:
        errors["description"] = []



    if not route_name:
        errors["route_name"].append("Trek name is required")

    if not location:
        errors["location"].append("Location is required")

    if difficulty not in ["Easy", "Moderate", "Tough"]:
        errors["difficulty"].append("Invalid difficulty")

    if not days_on_trail:
        errors["days_on_trail"].append("Duration is required")

    if not description:
        errors["description"].append("Description is required")

    if not altitude:
        errors["altitude"].append("Altitude is required")


    

    existing_route = TrekRoute.query.filter_by(route_name=route_name).first()

    if existing_route:                                           # to check if route exists
        errors["route_name"].append("Trek name already exists")



    for key in list(errors.keys()):    # to remove empty lists (of items from the dictionary)
        if not errors[key]:            # if the key is empty, remove it from the dictionary
            del errors[key]

    if errors:
        return jsonify({"errors": errors}), 400              



    from werkzeug.utils import secure_filename
    import os

    filename = secure_filename(image.filename)             #to get the image name

    image.save(os.path.join("static", "trek_images", filename))     #to save the image

    image = f"trek_images/{filename}"      #to store the image path
    
    new_trek_route = TrekRoute(
        route_name = trek_route_data.get("route_name"),
        location = trek_route_data.get("location"),
        difficulty = trek_route_data.get("difficulty"),
        days_on_trail = trek_route_data.get("days_on_trail"),
        description = trek_route_data.get("description"),
        altitude = trek_route_data.get("altitude"),
        image = image

    )

    db.session.add(new_trek_route)
    db.session.commit()

    return jsonify({"msg": "Trek created successfully", "trek_id": new_trek_route.id, "route_name": new_trek_route.route_name, "image": new_trek_route.image}), 200
    







@app.route("/api/admin/all_treks", methods = ["GET"])  # to get all created trek routes (from here admin can choose the trek he wants to view)
@roles_required('admin')

def get_all_treks():

    trek_routes = TrekRoute.query.all()
    result = []

    for trek in trek_routes:
        trek_data = {

            "trek_id": trek.id,
            "route_name": trek.route_name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "days_on_trail": trek.days_on_trail,
            "description": trek.description,
            "altitude": trek.altitude,
            "image" : trek.image
        }

        result.append(trek_data)

    return jsonify(trek_routes = result), 200







@app.route("/api/admin/routes/<int:route_id>", methods = ["GET"])  # to get trek route details using this route admin will schedule trek
@roles_required('admin')

def get_trek_route_details(route_id):

    trek_route = TrekRoute.query.get(route_id)

    if not trek_route:
        return jsonify({"msg": "Trek route does not exist"}), 400

    trek_route_data = {

        "route_id": trek_route.id,
        "route_name": trek_route.route_name,
        "location": trek_route.location,
        "difficulty": trek_route.difficulty,
        "days_of_trail": trek_route.days_of_trail,
        "description": trek_route.description,
        "altitude": trek_route.altitude,
        "price": trek_route.price,
    }

    return jsonify(trek_route = trek_route_data), 200







@app.route("/api/admin/routes/<int:route_id>/schedule", methods = ["POST"])  # to schedule trek
@roles_required('admin')

def schedule_trek(route_id):

    trek_route = TrekRoute.query.get(route_id)

    if not trek_route:
        return jsonify({"msg": "Trek route does not exist"}), 400

    schedule_data = request.get_json()

    start_date = schedule_data.get("start_date")
    end_date = schedule_data.get("end_date")
    total_slots = schedule_data.get("total_slots")
    price = schedule_data.get("price")

    errors = {}

    if "start_date" not in errors:
        errors["start_date"] = []

    if "end_date" not in errors:
        errors["end_date"] = []

    if "total_slots" not in errors:
        errors["total_slots"] = []
    
    if "price" not in errors:
        errors["price"] = []


    if not start_date:
        errors["start_date"].append("Start date is required")

    if not end_date:
        errors["end_date"].append("End date is required")

    if not total_slots:
        errors["total_slots"].append("Total slots is required")
    
    if not price:
        errors["price"].append("Price is required")

    for key in list(errors.keys()):    # to remove empty lists (of items from the dictionary)
        if not errors[key]:            # if the key is empty, remove it from the dictionary
            del errors[key]

    if errors:
        return jsonify({"errors": errors}), 400

    from datetime import datetime

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({
            "errors": {
                "start_date": ["Invalid date format"],
                "end_date": ["Invalid date format"]
            }
        }), 400

    trek = Trek(
        route_id = trek_route.id,
        trek_name = trek_route.route_name,
        start_date = start_date,
        end_date = end_date,
        total_slots = total_slots,
        available_slots = total_slots,
        price = price,
        status = "Open"
    )

    db.session.add(trek)
    db.session.commit()

    return jsonify({"msg": "Trek scheduled successfully", "trek_id": trek.id}), 200








@app.route("/api/admin/scheduled_treks", methods = ["GET"])  # to get all scheduled treks
@roles_required('admin')

def get_all_scheduled_treks():
    treks = Trek.query.all()
    result = []

    for trek in treks:
        trek_data = {
            "trek_id": trek.id,
            "trek_name": trek.trek_name,
            "start_date": trek.start_date.isoformat(),
            "end_date": trek.end_date.isoformat(),
            "total_slots": trek.total_slots,
            "available_slots": trek.available_slots,
            "price": trek.price,
            "status": trek.status
        }

        result.append(trek_data)

    return jsonify(treks = result), 200








@app.route("/api/admin/scheduled_trek/<int:trek_id>", methods = ["GET"])  # to get a scheduled trek details
@roles_required('admin')

def get_scheduled_trek(trek_id):
    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"msg": "Trek does not exist"}), 400

    trek_data = {
        "trek_id": trek.id,
        "trek_name": trek.trek_name,
        "start_date": trek.start_date.isoformat(),
        "end_date": trek.end_date.isoformat(),
        "total_slots": trek.total_slots,
        "available_slots": trek.available_slots,
        "price": trek.price,
        "status": trek.status
    }

    return jsonify(trek = trek_data), 200









@app.route("/api/admin/scheduled_treks/<int:trek_id>/update_trek", methods = ["PUT"])  # to update scheduled_trek details like update, cancel, complete, open, close
@roles_required('admin')

def update_scheduled_trek(trek_id):

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"msg": "Trek does not exist"}), 400

    trek_data = request.json

    if trek_data.get("start_date"):

        trek_data["start_date"] = datetime.strptime(trek_data["start_date"], "%Y-%m-%d").date()

    if trek_data.get("end_date"):

        trek_data["end_date"] = datetime.strptime(trek_data["end_date"], "%Y-%m-%d").date()




    trek.start_date = trek_data.get("start_date", trek.start_date)
    trek.end_date = trek_data.get("end_date", trek.end_date)
    trek.trek_name = trek_data.get("trek_name", trek.trek_name)
    trek.price = trek_data.get("price", trek.price)
    trek.status = trek_data.get("status", trek.status)
    trek.total_slots = trek_data.get("total_slots", trek.total_slots)
    trek.available_slots = trek_data.get("available_slots", trek.available_slots)

    db.session.commit()

    return jsonify({"msg": "Trek updated successfully"}), 200






@app.route("/api/admin/scheduled_treks/<int:trek_id>/delete_trek", methods = ["POST"])  # to delete scheduled_trek
@roles_required('admin')

def delete_scheduled_trek(trek_id):
    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"msg": "Trek does not exist"}), 400
    
    bookings = Booking.query.filter_by(trek_id = trek_id).all()

    for booking in bookings:
        booking.status = "Cancelled"        #if scheduled trek cancelled by admin , all users who have booked that trek will be cancelled

    db.session.delete(trek)
    db.session.commit()

    return jsonify({"msg": "Trek deleted successfully"}), 200








@app.route("/api/admin/bookings", methods = ["GET"])  # to get all bookings
@roles_required('admin')    

def get_all_bookings():
    bookings = Booking.query.all()

    total_bookings = Booking.query.filter_by(booking_status = "Booked").count()

    cancelled_bookings = Booking.query.filter_by(booking_status = "Cancelled").count()

    

    result = []


    for booking in bookings:
        
        assigned_staff = []  

        for staff_assignment in booking.trek.trek_staff_assignment:

            assigned_staff.append(staff_assignment.staff.username)

        trek_total_bookings = Booking.query.filter_by(trek_id = booking.trek_id, booking_status = "Booked").count()         #to count the total bookings for that trek

        trek_total_users_booked = Booking.query.filter_by(trek_id = booking.trek_id, booking_status = "Booked").count()       #to count the total users who have booked the trek

        
        trek_total_amount = 0
        trek_total_bookingss = Booking.query.filter_by(trek_id = booking.trek_id, booking_status = "Booked").all()
        
        for trek_booking in trek_total_bookingss:
            trek_total_amount += trek_booking.total_amount


        booking_data = {
            "booking_id": booking.id,
            "trekker": booking.trekker.username,   # booking and trekker(user model) has one to one relationship
            "trek_name": booking.trek.route.route_name,
            "booking_date": booking.booking_date.isoformat(),
            "trek_status" : booking.trek.status,          #open, closed
            "total_amount" : booking.total_amount,    
            "booking_status": booking.booking_status, #Booked ,   Cancelled
            "assigned_staff": assigned_staff,
            "trek_total_bookings": trek_total_bookings,
            "trek_total_users_booked": trek_total_users_booked,
            "trek_total_amount": trek_total_amount
            
        }
        result.append(booking_data)

    return jsonify(bookings = result, total_bookings = total_bookings, cancelled_bookings = cancelled_bookings), 200










@app.route("/api/admin/create_staff", methods=["POST"])  # to create new staff (admin first create a staff then only that staff can login and manage the trek)
@roles_required("admin")

def create_staff():
    staff_data = request.json

    errors = {}

    staff_name = staff_data.get("staff_name", None)
    staff_email = staff_data.get("staff_email", None)
    staff_phone = staff_data.get("staff_phone", None)
    staff_password = staff_data.get("staff_password", None)
    role = staff_data.get("role", None)


    if "staff_name" not in errors:
        errors["staff_name"] = []

    if "staff_email" not in errors:
        errors["staff_email"] = []

    if "staff_phone" not in errors:
        errors["staff_phone"] = []

    if "staff_password" not in errors:
        errors["staff_password"] = []

    if not staff_name:
        errors["staff_name"].append("Missing required field")

    if not staff_email:
        errors["staff_email"].append("Missing required field")

    if not staff_phone:
        errors["staff_phone"].append("Missing required field")

    if not staff_password:
        errors["staff_password"].append("Missing required field")

    if User.query.filter_by(username = staff_name).first():
        errors["staff_name"].append("Staff username already exists")

    if User.query.filter_by(email = staff_email).first():
        errors["staff_email"].append("Staff email already exists")

    if User.query.filter_by(phone = staff_phone).first():
        errors["staff_phone"].append("Staff phone number already exists")


    errors = {k: v for k, v in errors.items() if v}



    if errors:
        return jsonify(errors), 400
    
    

    staff = User(
        username = staff_data.get("staff_name"),
        email = staff_data.get("staff_email"),
        phone = staff_data.get("staff_phone"),
        password = generate_password_hash(staff_password),
        role = role
    )

    db.session.add(staff)
    db.session.commit()

    return jsonify({
        "msg": "Staff created successfully",
        "staff_id": staff.id
    }), 201








@app.route("/api/admin/treks/<int:trek_id>/assign_staff", methods = ["POST"])  # to assign staff to a trek
@roles_required('admin')

def assign_staff(trek_id):
    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"msg": "Trek does not exist"}), 400

    staff_data = request.json
    staff_id = staff_data.get("staff_id")

    if not staff_id:
        return jsonify({"msg": "Staff ID is required"}), 400

    staff = User.query.get(staff_id)

    if not staff:
        return jsonify({"msg": "Staff does not exist"}), 400

    trek_staff = TrekStaffAssignment(trek_id = trek_id, trek_staff_id = staff_id)

    db.session.add(trek_staff)
    db.session.commit()

    return jsonify({"msg": "Staff assigned successfully"}), 200








@app.route("/api/admin/treks/<int:trek_id>/staff", methods = ["GET"])  # to get all staff assigned to a trek
@roles_required('admin')

def get_assigned_staff(trek_id):
    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"msg": "Trek does not exist"}), 400

    assignments = TrekStaffAssignment.query.filter_by(trek_id = trek_id).all()
    result = []

    for assignment in assignments:
        staff_data = {
            "assignment_id": assignment.id,
            "staff_id": assignment.staff.id,
            "staff_name": assignment.staff.username,
            "staff_email": assignment.staff.email,
            "staff_phone": assignment.staff.phone
        }

        result.append(staff_data)

    return jsonify(assigned_staff = result), 200






@app.route("/api/admin/assignments/<int:assignment_id>", methods = ["POST"])  # to remove staff from a trek
@roles_required('admin')

def remove_staff(assignment_id):
    data  = request.json

    assignment = TrekStaffAssignment.query.filter_by(id = assignment_id, trek_id = data.get("trek_id")).first()

    if not assignment:
        return jsonify({"msg": "Staff Assignment does not exist"}), 400

    db.session.delete(assignment)
    db.session.commit()

    return jsonify({"msg": "Staff removed successfully"}), 200






@app.route("/api/admin/user_deactivate/<int:user_id>", methods = ["POST"])  # to deactivate user (trekker / staff)
@roles_required('admin')

def deactivate_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User does not exist"}), 400

    user.is_active = False
    db.session.commit()

    return jsonify({"msg": "User deactivated successfully"}), 200
    





@app.route("/api/admin/user_activate/<int:user_id>", methods = ["POST"])  # to reactivate user (trekker / staff)
@roles_required('admin')

def activate_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User does not exist"}), 400

    user.is_active = True
    db.session.commit()

    return jsonify({"msg": "User activated successfully"}), 200







@app.route("/api/admin/user_delete/<int:user_id>", methods = ["POST"])  # to delete a user(trekker / staff)
@roles_required('admin')

def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User does not exist"}), 400

    user.is_active = False
    user.is_deleted = True
    db.session.commit()

    return jsonify({"msg": "User deleted successfully"}), 200







@app.route("/api/admin/all_trekkers", methods = ["GET"])
@roles_required('admin')

def all_trekkers():
    trekkers = User.query.filter_by(role = "trekker", is_deleted = False).all()
    result = []

    for trekker in trekkers:
        trekker_data = {
            "id": trekker.id,
            "name": trekker.username,
            "email": trekker.email,
            "phone": trekker.phone,
            "is_active": trekker.is_active,
            "is_deleted": trekker.is_deleted
        }

        result.append(trekker_data)

    return jsonify(trekkers = result), 200







@app.route("/api/admin/all_staffs", methods = ["GET"])
@roles_required('admin')

def all_staffs():
    
    staffs = User.query.filter_by(role = "trek_staff", is_deleted = False).all()
    result = []

    for staff in staffs:
        staff_data = {
            "id": staff.id,
            "name": staff.username,
            "email": staff.email,
            "phone": staff.phone,
            "is_active": staff.is_active,
            "is_deleted": staff.is_deleted
        }

        result.append(staff_data)

    return jsonify(staffs = result), 200










@app.route("/api/admin/reports", methods = ["GET"])  # to get all reports
@roles_required('admin')

def get_reports():
    
    total_treks_routes = TrekRoute.query.count()
    total_scheduled_treks = Trek.query.filter_by(status = "Open").count()
    total_trekkers = User.query.filter_by(role = "trekker", is_active = True, is_deleted = False).count()
    total_staffs = User.query.filter_by(role = "trek_staff", is_active = True, is_deleted = False).count()
    total_bookings = Booking.query.filter_by(booking_status = "Booked").count()

    bookings = Booking.query.filter_by(booking_status = "Booked").all()
    total_revenue = 0
    for booking in bookings:
        total_revenue += booking.total_amount



    trek_routes = TrekRoute.query.all()

    result_trek_routes = []

    for trek_route in trek_routes:

        total_trek_bookings = 0

        for trek in trek_route.treks:
            for booking in trek.bookings:
                if booking.booking_status == "Booked":
                    total_trek_bookings += 1

        trek_route_data = {
            "id": trek_route.id,
            "route_name": trek_route.route_name,
            "location": trek_route.location,
            "total_bookings": total_trek_bookings
        }

        result_trek_routes.append(trek_route_data)




    trek_staffs = User.query.filter_by(role = "trek_staff").all()
    result_trek_staffs = []

    for trek_staff in trek_staffs:

        total_assigned_treks = TrekStaffAssignment.query.filter_by(trek_staff_id = trek_staff.id).count()

        trek_staff_data = {
            "id": trek_staff.id,
            "name": trek_staff.username,
            "email": trek_staff.email,
            "phone": trek_staff.phone,
            "is_active": trek_staff.is_active,
            "total_assigned_treks": total_assigned_treks
        }

        result_trek_staffs.append(trek_staff_data)
    


    
    bookings  = Booking.query.filter_by(booking_status = "Booked").all()
    
    result = {}
    for booking in bookings:

        trek_name = booking.trek.route.route_name

        if trek_name not in result:
            result[trek_name] = 0

        result[trek_name] += booking.total_amount


    result_trek_revenue = []

    for trek_name , revenue in result.items():

        result_trek_revenue.append({

            "trek_name": trek_name,
            "total_trek_revenue": revenue

        })


    return jsonify(total_treks_routes = total_treks_routes,
                   total_scheduled_treks = total_scheduled_treks,
                   total_trekkers = total_trekkers,
                   total_staffs = total_staffs,
                   total_bookings = total_bookings,
                   total_revenue = total_revenue,
                   result_trek_routes = result_trek_routes,
                   result_trek_staffs = result_trek_staffs,
                   result_trek_revenue = result_trek_revenue), 200



    