"""login module"""
from flask import request, session, redirect, render_template
from werkzeug.security import check_password_hash
import db

def user_login():
    """handling login"""
    error_message=""
    login = request.form.get('login')
    password = request.form.get('password')
    user = db.login_request(login)

    if not user:
        error_message="user dose not exist"
    else:
        hash_value = user.password
        if not check_password_hash(hash_value, password):
            error_message="invalid password"
        else:
            users_id = user.id
            session["id"] = users_id
            receiver = session["receiver"]
            return redirect(f"/id{users_id}/send{receiver}")
    return render_template('index.html', message=error_message)

def logout():
    """handling logout"""
    del session["id"]
    return redirect("/")
