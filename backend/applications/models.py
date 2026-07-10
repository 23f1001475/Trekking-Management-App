from .database import db

from datetime import datetime, timezone # (to show created_at in UTC(universal coordinated time) timezone)


#User model : Role based access. Userd for : Admin, Trek Staff and Trekker
class User(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), nullable = False, unique = True)
    role = db.Column(db.String(), nullable = False, default = "trekker")
    phone = db.Column(db.String(), nullable = False, unique = True)
    is_active = db.Column(db.Boolean, nullable = False, default = True)
    created_at = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now(timezone.utc))                  #usign lambda function to set created_at in UTC timezone as datetime.utcnow() returns time in UTC timezone but without timezone info, so we use lambda function to set created_at with timezone info.
    updated_at = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now(timezone.utc), onupdate = lambda: datetime.now(timezone.utc)) #onupdate is used to update the updated_at field whenever the user is updated. timezone = True is to make the datetime object timezone aware. if timezone = False, the datetime object will be timezone naive.
    is_deleted = db.Column(db.Boolean, default = False)
    deleted_at = db.Column(db.DateTime) 
    bookings = db.relationship("Booking", backref = "trekker", lazy = True)  # one to many , one trekker --> many bookings | one Booking --> one trekker
    assigned_treks = db.relationship("TrekStaffAssignment", backref = "staff", lazy = True) # many to one
    activity_logs = db.relationship("ActivityLog", backref = "user", lazy = True)


#Trek Route Model : To manage trekking routes.

class TrekRoute(db.Model):
    __tablename__ = "trek_route"
    id  = db.Column(db.Integer, primary_key = True)
    route_name = db.Column(db.String(), nullable = False)
    location = db.Column(db.String(), nullable = False)
    difficulty = db.Column(db.String(), nullable = False)  # Easy, Moderate or Difficult
    days_on_trail = db.Column(db.Integer, nullable = False)
    altitude = db.Column(db.Integer, nullable = False)
    description = db.Column(db.Text, nullable = False)
    image = db.Column(db.String(), nullable = True)
    is_active = db.Column(db.Boolean, nullable = False, default = True)
    created_at = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now(timezone.utc), onupdate = lambda: datetime.now(timezone.utc))
    treks = db.relationship("Trek", backref = "route", lazy = True)



#Trek Model : scheduled treks.

class Trek(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    route_id = db.Column(db.Integer, db.ForeignKey("trek_route.id"), nullable = False)
    trek_name = db.Column(db.String(), nullable = False)
    start_date = db.Column(db.Date, nullable = False)
    end_date = db.Column(db.Date, nullable = False)
    total_slots = db.Column(db.Integer, nullable = False)
    available_slots = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Numeric(precision = 10, scale = 2), nullable = False)
    status = db.Column(db.String(), default = "Open")   #Open, Closed
    created_at = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now(timezone.utc), onupdate = lambda: datetime.now(timezone.utc))
    bookings = db.relationship("Booking", backref = "trek", lazy = True)
    trek_staff_assignment = db.relationship("TrekStaffAssignment", backref = "trek", lazy = True, cascade = "all, delete-orphan") # one to many, one trek --> many staff assignment | one staff assignment --> one trek


# Booking Model : to store trek registrations.

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    trek_id = db.Column(db.Integer, db.ForeignKey("trek.id"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    booking_date = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now(timezone.utc), onupdate = lambda: datetime.now(timezone.utc))  # to show the last modification time(when the booking rocord was last changed)
    booking_status = db.Column(db.String(), default = "Not Booked") 
    participants = db.Column(db.Integer, default = 1)
    total_amount = db.Column(db.Numeric(precision = 10, scale = 2), nullable = False)



# Trek Staff Assignment Model: to mananage staff. many staff can be assigned to one trek. One staff can manage many trek (many to many (staff <-> trek))

class TrekStaffAssignment(db.Model):
    __tablename__ = "trek_staff_assignment"
    id = db.Column(db.Integer, primary_key = True)
    trek_id = db.Column(db.Integer, db.ForeignKey("trek.id"), nullable = False)
    trek_staff_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    assigned_at = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now(timezone.utc))




# Activity loig Model : for Admin Reports.

class ActivityLog(db.Model):
    __tablename__ = "activity_log"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    action = db.Column(db.String(), nullable = False)   # trek_created, staff_created, staff_updated, booking_createed etc
    created_at = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now(timezone.utc))
