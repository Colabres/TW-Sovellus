from flask import request, session, redirect, render_template
from werkzeug.security import check_password_hash, generate_password_hash
import db

def login():
    error_message=""
    login = request.form.get('login')
    password = request.form.get('password')
    user = db.login_request(login)
    id = user.id
    if not user:
        error_message="user dose not exist"
    else:
        hash_value = user.password
    if check_password_hash(hash_value, password):
        session["id"] = id
        receiver = session["receiver"]
        return redirect(f"/id{id}/send{receiver}")
    else:
        error_message="invalid password"
    if error_message:
        return render_template('index.html', message=error_message)