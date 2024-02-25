from flask import request,render_template,redirect,session
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from app import app
from db import db
import re



def register_form():
    action = request.form.get('action')
    if action == 'register':
        # Handle registration logic
        def invalid_password(password):
            pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).+$')
            return not bool(pattern.match(password))

        def invalid_username(login):
            sql = text("SELECT * FROM users WHERE login=:login")
            result = db.session.execute(sql, {"login":login})
            exists = bool(result.fetchone())
            return exists

        new_login = request.form.get('login')
        new_password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        error_message= ""

        if len(new_login) < 5:
            error_message="username is to short."
        elif invalid_username(new_login):
            error_message="username allready taken"
        elif len(new_password) < 5:
            error_message="password is to short"
        elif invalid_password(new_password):
            error_message="invalid password"

        if error_message:
            return render_template('register.html', message=error_message)
        else:
            hash_value = generate_password_hash(new_password)

            sql = text("INSERT INTO users (login, password) VALUES (:login, :password)")
            db.session.execute(sql, {"login": new_login, "password": hash_value})
            db.session.commit()

            sql = text("SELECT id FROM users WHERE login=:login")
            result = db.session.execute(sql, {"login": new_login})
            user = result.fetchone()

            id = user.id
            sql = text("""INSERT INTO profile
                        (user_id, firstname, lastname)
                        VALUES (:id, :firstname, :lastname)""")
            db.session.execute(sql, {"id": id, "firstname": firstname, "lastname": lastname})
            db.session.commit()

            session["id"] = id
            session["receiver"] = 0
            receiver = session["receiver"]
            return redirect(f"/id{id}/send{receiver}")