"""module for register"""
from flask import request,render_template,redirect,session
from werkzeug.security import generate_password_hash
import db


def register_form():
    """handeling register form"""
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

    hash_value = generate_password_hash(new_password)
    user=db.insert_user(new_login,hash_value)

    user_id = user.id
    db.insert_profile(user_id,firstname,lastname)

    session["id"] = user_id
    session["receiver"] = 0
    receiver = session["receiver"]
    return redirect(f"/id{user_id}/send{receiver}")
        