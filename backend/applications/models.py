from .database import db
from flask_security import UserMixin, RoleMixin   #these are class woth have predefined methods(functions) which are necessary to retreive the authentication token
from datetime import datetime


#User model : Role based access. Userd for : Admin, Trek Staff and Trekker
class User(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), nullable = False, unique = True)
    role = db.Column(db.String(), nullable = False, default = "trekker")
    phone = db.Column(db.Integer(), nullable = False, unique = True)
    is_active = db.Column(db.Boolean, nullable = False, default = True)
    created_at = db.Column(db.DataTime, default = datetime.utcnow)
    is_blaclisted = db.Column(db.Boolean, default = False)
    is_deleted = db.Column(db.Boolean, default = False)
    deleted_at = db.Column(db.DateTime) 
    bookings = db.relationship("Booking", backref = "trekker", lazy = True)  # one to many , one trekker --> many bookings | one Booking --> one trekker
    assigned_treks = db.relationship("TrekStaffAssignment", backref = "staff", lazy = True) # many to one


#Trek Route Model : To manage trekking routes.

class TrekRoute(db.Model):
    id  = db.Column(db.Integer, primary_key = True)
    route_name = db.Column(db.String(), nullable = False)
    location = db.Column(db.String(), nullable = False)
    difficulty = db.Column(db.String(), nullable = False)  # Easy, Moderate or Difficult
    days_on_trail = db.Column(db.Integer, nullable = False)
    altitude = db.Column(db.Integer, nullable = False)
    description = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DataTime, default = datetime.utcnow)
    treks = db.relationship("Trek", backref = "route", lazy = True)


#Trek Model : scheduled treks.

class Trek(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    route_id = db.Column(db.Integer, db.ForeignKey("trek_route.id"))
    start_date = db.Column(db.Date, nullable = False)
    end_date = db.Column(db.Date, nullable = False)
    total_slots = db.Column(db.Integer, nullable = False)
    available_slots = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)
    status = db.column(db.String(), default = "Open")   #Open, Closed, Cancelled, Completed
    approval_status = db.Column(db.string(), default = "Approved") #Approved or Rejected or Waiting
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    bookings = db.relationship("Booking", backref = "trek", lazy = True)
    trek_staff_assignment = db.relationship("TrekStaffAssignment", backref = "trek", lazy = True)


# Booking Model : to store trek registrations.

class Booking(db.MOdel):
    id = db.Column(db.Integer, primary_key = True)
    trek_id = db.Column(db.Integer, db.ForeignKey("trek.id"), nullable = False)
    user_id = db.Column(db.Integer, db.Foreignkey("user.id"), nullable = False)
    booking_date = db.Column(db.DateTime, default = datetime.utcnow)
    booking_status = db.Column(db.String(), default = "Pending") #Pending, Confirmed, Cancelled, Completed
    participants = db.Column(db.Integer, default = 1)
    total_amount = db.Column(db.Float, nullable = False)


# Trek Staff Assignment Model: to mananage staff. many staff can be assigned to one trek. One staff can manage many trek (many to many (staff <-> trek))

class TrekStaffAssignment(db.Model):
    __tablename__ = "trek_staff_assignment"
    id = db.Column(db.Integer, primary_key = True)
    trek_id = db.Column(db.integer, db.ForeignKey("trek.id"), nullable = False)
    trek_staff_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    assigned_at = db.Column(db.DateTime, default = datetime.utcnow)


# Activity loig Model : for Admin Reports.

class ActivityLog(db.MOdel):
    __tablename__ = "activity_log"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    action = db.Column(db.String(), nullable = False)   # trek_created, staff_created, staff_updated, booking_createed etc
    created_at = db.Column(db.DateTime, default = datetime.utcnow)


#Notification Model : for Celery tasks. for Trek approved, Booking confirmed, Trek cancelled.

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    message_title = db.Column(db.String(), nullable = False)
    message_body = db.Column(db.Text, nullable = False)
    is_read = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)