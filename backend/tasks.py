
from celery_worker import celery_app  #cenelry_workker is calling app and task is callign cecelery_app (to prevent circular import error)

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText    #for sneding text, html type contents
import smtplib 

from flask import render_template
from applications.models import *

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025         #default smtp port for mailhog
SENDER_ADDRESS = 'vivekmittal@gmail.com'
SENDER_PASSWORD = ''



def send_email(to_address,subject,message,content="text",attachment=None):     #message can be html or text
    
    msg = MIMEMultipart()
    msg['To']=to_address       #will fetch form the database
    msg['From']=SENDER_ADDRESS
    msg['Subject']=subject
    if content == "html":
        msg.attach(MIMEText(message,'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    if attachment:
        with open(attachment,"rb") as a:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(a.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment: filename={attachment}")
        msg.attach(part)          

    s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT )
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return True



@celery_app.task                           #Monthly trekking activity report for Admin (HTML). 
def send_monthly_user_report():
    
    admin = User.query.filter_by(role = "admin").first()
    if not admin:
        return "No admin found"
    
    total_completed_treks = Trek.query.filter_by(status = "Completed").count()
   
    total_cancelled_treks = Trek.query.filter_by(status = "Cancelled").count()

    total_active_treks = Trek.query.filter_by(status = "Open").count()
    
    total_active_trekkers = User.query.filter_by(role = "trekker", is_active = True, is_deleted = False).count()
    
    total_active_staff = User.query.filter_by(role = "trek_staff", is_active = True, is_deleted = False).count()
    
    overall_bookings = Booking.query.filter_by(booking_status = "Booked").count()

    bookings = Booking.query.filter_by(booking_status = "Booked").all()


    overall_revenue = 0
    for booking in bookings:
        overall_revenue += booking.total_amount


 

    trek_routes = TrekRoute.query.all()

    popular_trek_routes = []

    for trek_route in trek_routes:
        total_trek_bookings = 0
        price = 0

        for trek in trek_route.treks:

            price = trek.price
            for booking in trek.bookings:
                if booking.booking_status == "Booked":
                    total_trek_bookings += 1

        

        popular_trek_route_data = {
            "id" : trek_route.id,
            "route_name" : trek_route.route_name,
            "location" : trek_route.location,
            "difficulty" : trek_route.difficulty,
            "days_on_trail" : trek_route.days_on_trail,
            "altitude" : trek_route.altitude,
            "price" : price,
            "total_bookings" : total_trek_bookings
        }

        popular_trek_routes.append(popular_trek_route_data)




    trek_staffs = User.query.filter_by(role = "trek_staff").all()
    most_active_trek_staffs = []

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

        most_active_trek_staffs.append(trek_staff_data)




    bookings  = Booking.query.filter_by(booking_status = "Booked").all()
    
    result = {}
    for booking in bookings:

        trek_name = booking.trek.route.route_name

        if trek_name not in result:
            result[trek_name] = 0

        result[trek_name] += booking.total_amount


    result_trek_revenue = []           #trek with highest revenue

    for trek_name , revenue in result.items():

        result_trek_revenue.append({  "trek_name": trek_name, "total_trek_revenue": revenue })

    
    html = render_template("montly_trekking_report_admin.html",
                            total_completed_treks = total_completed_treks,
                            total_cancelled_treks = total_cancelled_treks,
                            total_active_treks = total_active_treks,
                            total_active_trekkers = total_active_trekkers,
                            total_active_staff = total_active_staff,
                            overall_bookings = overall_bookings,
                            overall_revenue = overall_revenue,
                            popular_trek_routes = popular_trek_routes,
                            most_active_trek_staffs = most_active_trek_staffs,
                            result_trek_revenue = result_trek_revenue)

    send_email(admin.email, "Monthly User Report",html, content = "html") 
    # send_email("vivekmittal@gmail.com","Monthly user report","This is the monthly user report")

    return "Monthly user report sent"






@celery_app.task                             # Daily reminder job for upcoming treks (Email) --> to user
def send_daily_reminder():


    bookings = Booking.query.filter_by(booking_status = "Booked").all()
    


    for booking in bookings:

        user = User.query.get(booking.user_id)

        trek = Trek.query.get(booking.trek_id)


    html = render_template("user_daily_reminder.html", user = user, trek = trek)
    send_email(user.email, "Upcoming Trek Reminder", html ,  content = "html")

    # send_email("vivekmittal@gmail.com","Daily reminder","This is the daily reminder")
    return "Daily reminder sent"



import csv

@celery_app.task                          #this is for the user-triggered tasks : User-triggered CSV export for trekking history.

def export_user_history_csv(user_id):
    
    user = User.query.get(user_id)
    if not user:
        return False
    
    bookings = Booking.query.filter_by(user_id = user.id).order_by(Booking.booking_date.desc()).all()

    name = user.username


    filename = f"user_history/{name}_history.csv"


    with open (filename, "w", newline = "") as f:

        writer = csv.writer(f)

        writer.writerow([ "Username", "Booking ID", "Trek ID", "Trek Name", "Booking Date", "Start Date",  "End Date", "Price", "Booking Status", "Trek Status"])


        for booking in bookings:
            if booking.booking_status in ['Booked', 'Cancelled']:

                writer.writerow([
                    user.username,
                    booking.id,
                    booking.trek.id,
                    booking.trek.route.route_name,
                    str(booking.booking_date.isoformat()),
                    str(booking.trek.start_date.isoformat()),       
                    str(booking.trek.end_date.isoformat()),
                    booking.total_amount,
                    booking.booking_status,
                    booking.trek.status   
                ])
            
    send_email(user.email,subject  = "Trekking History CSV", message = "please find oyur trekking history attached", content = "text", attachment = filename)   
    return filename
