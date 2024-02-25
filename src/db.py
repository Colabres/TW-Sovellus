from flask import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import re

db = SQLAlchemy()

def login_request(login):
    sql = text("SELECT id, password FROM users WHERE login=:login")
    result = db.session.execute(sql, {"login":login})
    user = result.fetchone()
    
    return user

def invalid_username(login):
    sql = text("SELECT * FROM users WHERE login=:login")
    result = db.session.execute(sql, {"login":login})
    exists = bool(result.fetchone())
    return exists

def invalid_password(password):
    pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).+$')
    return not bool(pattern.match(password))

def insert_user(new_login,hash_value):
    sql = text("INSERT INTO users (login, password) VALUES (:login, :password)")
    db.session.execute(sql, {"login": new_login, "password": hash_value})
    db.session.commit()

    sql = text("SELECT id FROM users WHERE login=:login")
    result = db.session.execute(sql, {"login": new_login})
    user = result.fetchone()

    return user

def insert_profile(id,firstname,lastname):
    sql = text("""INSERT INTO profile
                (user_id, firstname, lastname)
                VALUES (:id, :firstname, :lastname)""")
    db.session.execute(sql, {"id": id, "firstname": firstname, "lastname": lastname})
    db.session.commit()

def dialogue_request(id,receiver):
    sql = text("""SELECT M.message, M.sender_id, P.firstname, P.lastname, F.file_name
                   FROM message M JOIN profile P ON M.sender_id = P.user_id 
                   LEFT JOIN photos F ON P.user_id = F.user_id 
                   WHERE sender_id=:id1 AND receiver_id=:id2 OR sender_id=:id3 
                   AND receiver_id=:id4 ORDER BY M.id""")
    result = db.session.execute(sql, {"id1": id, "id2": receiver, "id3": receiver, "id4": id})
    messages = result.fetchall()

    sql = text("""SELECT M.message, M.sender_id, M.receiver_id, receiver.firstname
                   AS receiver_firstname, receiver.lastname AS receiver_lastname, R.file_name
                   AS receiver_photo, sender.firstname AS sender_firstname, sender.lastname
                   AS sender_lastname, S.file_name AS sender_photo, M.id, P.user_id
                   FROM message M JOIN profile P ON M.sender_id = P.user_id JOIN profile sender
                   ON M.sender_id = sender.user_id JOIN profile receiver
                   ON M.receiver_id = receiver.user_id LEFT JOIN photos R
                   ON R.user_id = M.receiver_id LEFT JOIN photos S ON S.user_id = M.sender_id
                   WHERE sender_id=:id1
                   OR receiver_id=:id1 ORDER BY M.id DESC""")
    result2 = db.session.execute(sql, {"id1": id})
    contacts = result2.fetchall()
    return (messages,contacts)

def insert_message(id,receiver,message):
    sql = text("""INSERT INTO message
            (sender_id, receiver_id, message)
            VALUES (:id1, :id2, :message)""")
    db.session.execute(sql, {"id1": id, "id2": receiver, "message": message})
    db.session.commit()

def request_profile(profile_id):
    id = session["id"]
    sql = text("SELECT firstname, lastname, message, user_id FROM profile WHERE user_id=:id")
    result = db.session.execute(sql, {"id": profile_id})
    user = result.fetchone()

    sql2 = text("SELECT contact_id FROM contact WHERE user_id=:id")
    result2 = db.session.execute(sql2, {"id": id})
    contact = result2.fetchone()

    sql3 = text("SELECT file_name FROM photos WHERE user_id=:id ORDER BY id DESC")
    result3 = db.session.execute(sql3, {"id": id})
    photo = result3.fetchone()

    return (user,contact,photo)

def search_request(name):
    sql = text("SELECT * FROM profile WHERE firstname=:name")
    result = db.session.execute(sql, {"name": name})
    users = result.fetchall()
    return users

def update_profile(id,firstname,lastname,message):
    sql = text("""UPDATE profile SET firstname=:firstname, lastname=:lastname,
                    message=:message WHERE user_id=:id""")
    db.session.execute(sql, {"firstname": firstname,
                        "lastname": lastname, "message": message, "id": id})
    db.session.commit()

def request_profile_info(id):
    sql = text("SELECT firstname, lastname, message FROM profile WHERE user_id=:id")
    result = db.session.execute(sql, {"id": id})
    user = result.fetchone()
    return user

def get_photo(id):
    sql3 = text("SELECT file_name FROM photos WHERE user_id=:id ORDER BY id DESC")
    result3 = db.session.execute(sql3, {"id": id})
    photo = result3.fetchone()
    return photo

def insert_photo(id,name):
    sql = text("""INSERT INTO photos (user_id, file_name)
            VALUES (:id, :filename) ON CONFLICT (user_id) 
            DO UPDATE SET file_name = EXCLUDED.file_name""")
    db.session.execute(sql, {"id": id, "filename": name})
    db.session.commit()

def get_contacts(id):
    sql = text("""SELECT P.firstname, P.lastname, P.message, P.user_id,
                F.file_name FROM contact C JOIN profile P 
                ON C.contact_id = P.user_id LEFT JOIN photos F
                ON F.user_id=C.contact_id  WHERE C.user_id=:id""")
    result = db.session.execute(sql, {"id": id})

    contacts = result.fetchall()
    return contacts

def insert_contact(id,contact_id):
    sql = text("INSERT INTO contact (user_id, contact_id) VALUES (:id1, :id2)")
    db.session.execute(sql, {"id1": id, "id2": contact_id})
    db.session.commit()