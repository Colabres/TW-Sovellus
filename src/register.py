from flask import request,render_template,redirect,session
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from app import app
import db
import re



def register_form():
    action = request.form.get('action')
    if action == 'register':
        # Handle registration logic
        new_login = request.form.get('login')
        new_password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        error_message= ""

        if len(new_login) < 5:
            error_message="username is to short."
        elif db.invalid_username(new_login):
            error_message="username allready taken"
        elif len(new_password) < 5:
            error_message="password is to short"
        elif db.invalid_password(new_password):
            error_message="invalid password"

        if error_message:
            return render_template('register.html', message=error_message)
        else:
            hash_value = generate_password_hash(new_password)
            user=db.insert_user(new_login,hash_value)

            id = user.id
            db.insert_profile(id,firstname,lastname)


            session["id"] = id
            session["receiver"] = 0
            receiver = session["receiver"]
            return redirect(f"/id{id}/send{receiver}")