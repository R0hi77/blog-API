"""
Handles Sign up, Login and Log out endpoints 
"""

from flask import (
    Blueprint, request,session,g,jsonify
                   )
from werkzeug.security import generate_password_hash, check_password_hash

from .database import get_db
from flask_jwt_extended import create_access_token,create_refresh_token


authbp = Blueprint("auth",__name__,url_prefix="/api/auth")

@authbp.post('/register')
def register():
    username =request.form['username']
    password = request.form['password']
    error = None
    db = get_db()

    if username is None:
        error = "username required"
        return jsonify(
            {
                "message":error
            }
        )
    
    if password is None:
        error = "password is required"
        return jsonify(
            {
                "message":error
            }
        )
    
    if error is None:
        try:
            db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
             )
            db.commit()
            new_user =db.execute(
                "SELECT * FROM user WHERE username = ?",(username,)
            ).fetchone()
            message = "user created succesfully"
            return jsonify(
                {   "message":message,
                    "user":username,
                    "user_id":new_user['id']
                }
            )
        except db.IntegrityError:
            error=f"user {username} is already taken"
            return jsonify(
                {
                    "message":error
                }
            )
        
@authbp.post ("/login")
def login():
    username= request.form['username']
    password= request.form['password']
    error = None
    db = get_db()

    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    if user is None:
        error= "incorrect username, Try again"
        return jsonify(
            {
                "message":error
            }
        )
    
    elif not check_password_hash(user['password'],password):
        error = "incorrect password"
        return jsonify(
            {"message":error}

                       )
    
    if error is None:
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        session.clear()
        session['user_id']= user['id']
        
        return jsonify(
            {   
                "message": f"user {username} login succesfuly",

                "user_id":user['id'],
                
                "access_token":access_token,

                "refresh token":refresh_token
            }
        )
    
    
@authbp.get("/logout")
def logout():
    session.clear()
    return jsonify(
            {
                "message":"user logged out"
            }
        )
    
        
        
    


        

    
    
            
        

    