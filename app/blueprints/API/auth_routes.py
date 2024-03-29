from . import bp as api
from datetime import datetime, timedelta
from app import db
from app.models import User
from flask import make_response, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies
import re

#accepts a request with {"username": <desired username>, "password": <desired password>, 
#"email": <desired email address>}. If username or email are shared with a pre-existing user, 
#no account will be created.
#Returns an access token, as though the user just signed in.
@api.post('/register')
def register():
    content, response = request.json, {}
    print(content)
    valid = True;
    content["username"] = content["username"].strip()[0:30]
    content["email"] = content["email"].lower()
    if User.query.filter_by(email=content['email']).first():
      response['email error']=f'{content["email"]} is already taken/ Try again'
      valid = False;
    if User.query.filter_by(username=content['username']).first():
      response['username error']=f'{content["username"]} is already taken/ Try again'
      valid = False;
    if 'password' not in content:
       response['message'] = "Please include password"
       valid;
    allow_username= re.compile('^[A-Za-z0-9_]{5,30}$')
    if not allow_username.search(content['username']):
      response['username validity error'] = f'{content["username"]} is an invalid username. Please pick a username that is only letters, numbers, and underscores, and is between 5-30 characters in length.'
      valid = False;
    allow_email=re.compile('^[a-z0-9]+@[a-z]+\.[a-z]{2,3}$');
    if not allow_email.search(content['email']):
       response['email validity error'] = f'{content["email"]} is an invalid email.'
       valid = False;
    if valid:
        u = User(username = content["username"], admin = False, email = content["email"])
        print(u)
        
        u.hash_password(content["password"])
        u.commit()
        response = make_response(jsonify({'Success': f'User account created for {u.username}.'}))
        access_token = create_access_token(identity = content["username"])
        set_access_cookies(response, access_token)
       
        return response,200
    else:
        return jsonify(response), 400


#Accepts a request with {"username": <user's username>, "password": <user's password>}. Returns an access token that is used for verification by JWT, along with the other information used by the program.
@api.post('/signin')
def sign_in():
   
   username, password = request.json.get('username').strip(), request.json.get('password')
   user = User.query.filter_by(username=username).first()
   if user and user.check_password(password):
      response = {}
      response["username"] = username
      response["email"] = user.email
      response["admin"] = user.admin
      response["token"] =  create_access_token(identity=username)
    
      return jsonify(response), 200
   else:
      return jsonify({'Error':'Invalid Username or Password / Try Again'}), 400

#Requires no input, and unsets the Access Token you were using. 
@api.post('/logout')
def logout():
   response = jsonify({'Success':'Successful Logout'})
   unset_jwt_cookies(response)
   return response

@api.post('/check')
@jwt_required()
def check_token():
   return jsonify({"msg": "Successful authentication"}), 200

@api.after_request
def refresh_expiring_jwts(response):
    try:
        print("Working")
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now
        target_timestamp = datetime.timestamp(now() + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            response.json["token"] = create_access_token(identity=get_jwt_identity())
            print("resetting token")
            
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response
    

@api.get('/test')
def test():
   response = jsonify({"test": "successful"})
   return response