from flask import Flask, jsonify, request, current_app as app, abort
from applications.models import *
from flask_jwt_extended import create_access_token, jwt_required, current_user, get_jwt, verify_jwt_in_request
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash



@app.route('/api/login', methods = ["POST"])
def login():
    username = request.json.get("username", None) # None because if username is not provided, it will be None
    password = request.json.get("password", None)

    user = User.query.filter_by(username = username).first()
    if not user:
        user = User.query.filter_by(email = username).first()  # if username is not found, check if email is provided instead
    
    if not user or not (check_password_hash(user.password, password)): 
        return jsonify({"msg": "Bad username or password"}), 400
    
    if not user.is_active:
        return jsonify({"msg": "your account is deactivated, please contact admin"}), 403
    
    if user.is_deleted:
        return jsonify({"msg": "your account is deleted, please contact admin"}), 403
    
    access_token = create_access_token(identity = str(user.id), additional_claims={"role": user.role}) # identity is the unique identifier for the user, in this case, we are using the user id as the identity
    return jsonify(access_token = access_token, role = user.role, user = {"id": user.id, "username": user.username}), 200




@app.route("/api/register", methods = ["POST"])
def register():
    
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    phone = request.json.get("phone", None)
    role = request.json.get("role", None)

    errors = {}
    if "username" not in errors:
        errors["username"] = []

    if not username:
        errors["username"].append("username is required")

    if User.query.filter_by(username = username).first():
        errors["username"].append("username already exists")

    if "password" not in errors:
        errors["password"] = []

    if not password:
        errors["password"].append("password is required")

    if "email" not in errors:
        errors["email"] = []

    if not email:
        errors["email"].append("email is required")

    if User.query.filter_by(email = email).first():
        errors["email"].append("email already exists")

    if "phone" not in errors:
        errors["phone"] = []

    if not phone:
        errors["phone"].append("phone number is required")

    if User.query.filter_by(phone = phone).first():
        errors["phone"].append("phone number already exists")


    if errors:
        return jsonify(errors), 400
    
    
    if not username or not password or not email or not phone or not role:
        return jsonify({"msg": "Missing required fields"}), 400
    
    if User.query.filter_by(username = username).first():
        return jsonify({"msg": "Username already exists"}), 400
    
    if User.query.filter_by(email = email).first():
        return jsonify({"msg": "Email already exists"}), 400
    
    if User.query.filter_by(phone = phone).first():
        return jsonify({"msg": "Phone number already exists"}), 400
    

    user = User(username = username, password = generate_password_hash(password), email = email, phone = phone, role = role)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 200




def roles_required(*roles):    # * is used to pass multiple roles as arguments to the decorator function for e.g. @roles_required("admin", "trek_staff" and "trekker") means that the user must have either "admin" or "trek_staff" role to access the resource
    def wrapper(fn):    #fn is the function that is being decorared with @roles_required(*roles)

        @wraps(fn)       # wraps is used to preserve the original function name (fn) and Without it, Flask might think every route function is called "wrapper"
        def decorator(*args, **kwargs):   #This is the function that actually executes when the route is called. It checks if the user has the required role and then calls the original function (fn) if the user has the required role, otherwise it returns a 403 error.
                                          #args(positional arguments) and kwargs(keyword arguments) 
            verify_jwt_in_request()    #checks whether a valid jwt extsts in the request header or not, if not it will return a 401 error
            claims = get_jwt()           #returns the payload(content) of the jwt
            if claims["role"] not in roles:
                return jsonify({ "msg" : "You do not have access to this resource" }), 403
            return fn(*args , **kwargs)   #calls the original function (fn) with the original arguments (args and kwargs)

        return decorator
    return wrapper       
            


@app.route("/api/logout", methods = ["POST"])
@jwt_required()
def logout():

    return jsonify({"msg": "Successfully logged out"}), 200


