"""database module"""
import re
from flask import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


db = SQLAlchemy()

def login_request(login):
    """request login info"""
    sql = text("SELECT id, password FROM users WHERE login=:login")
    result = db.session.execute(sql, {"login":login})
    user = result.fetchone()

    return user

def invalid_username(login):
    """checking if user exist"""
    sql = text("SELECT * FROM users WHERE login=:login")
    result = db.session.execute(sql, {"login":login})
    exists = bool(result.fetchone())
    return exists

def invalid_password(password):
    """checking if valid pasword"""
    pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).+$')
    return not bool(pattern.match(password))

def insert_user(new_login,hash_value):
    """adding new user to database"""
    sql = text("INSERT INTO users (login, password) VALUES (:login, :password)")
    db.session.execute(sql, {"login": new_login, "password": hash_value})
    db.session.commit()

    sql = text("SELECT id FROM users WHERE login=:login")
    result = db.session.execute(sql, {"login": new_login})
    user = result.fetchone()

    return user

def insert_profile(users_id,firstname,lastname):
    """adding profile info"""
    sql = text("""INSERT INTO profile
                (user_id, firstname, lastname)
                VALUES (:id, :firstname, :lastname)""")
    db.session.execute(sql, {"id": users_id, "firstname": firstname, "lastname": lastname})
    db.session.commit()

def dialogue_request(users_id,receiver):
    """requesting dialogue info"""
    sql = text("""SELECT M.message, M.sender_id, P.firstname, P.lastname, F.file_name
                   FROM message M JOIN profile P ON M.sender_id = P.user_id 
                   LEFT JOIN photos F ON P.user_id = F.user_id 
                   WHERE sender_id=:id1 AND receiver_id=:id2 OR sender_id=:id3 
                   AND receiver_id=:id4 ORDER BY M.id""")
    result = db.session.execute(sql, {"id1": users_id, "id2": receiver,
                                       "id3": receiver, "id4": users_id})
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
    result2 = db.session.execute(sql, {"id1": users_id})
    contacts = result2.fetchall()
    return (messages,contacts)

def insert_message(users_id,receiver,message):
    """adding message to database"""
    sql = text("""INSERT INTO message
            (sender_id, receiver_id, message)
            VALUES (:id1, :id2, :message)""")
    db.session.execute(sql, {"id1": users_id, "id2": receiver, "message": message})
    db.session.commit()

def request_profile(profile_id):
    """requesting profile info"""
    users_id = session["id"]
    sql = text("SELECT firstname, lastname, message, user_id FROM profile WHERE user_id=:id")
    result = db.session.execute(sql, {"id": profile_id})
    user = result.fetchone()

    sql2 = text("SELECT contact_id FROM contact WHERE user_id=:id")
    result2 = db.session.execute(sql2, {"id": users_id})
    contact = result2.fetchone()

    sql3 = text("SELECT file_name FROM photos WHERE user_id=:id ORDER BY id DESC")
    result3 = db.session.execute(sql3, {"id": users_id})
    photo = result3.fetchone()

    return (user,contact,photo)

def search_request(name):
    """requesting search results from database"""
    sql = text("SELECT * FROM profile P LEFT JOIN photos F ON P.user_id = F.user_id WHERE firstname=:name")
    result = db.session.execute(sql, {"name": name})
    users = result.fetchall()
    return users

def update_profile(users_id,firstname,lastname,message):
    """updating profile info"""
    sql = text("""UPDATE profile SET firstname=:firstname, lastname=:lastname,
                    message=:message WHERE user_id=:id""")
    db.session.execute(sql, {"firstname": firstname,
                        "lastname": lastname, "message": message, "id": users_id})
    db.session.commit()

def request_profile_info(users_id):
    """requesting non confident user info"""
    sql = text("SELECT firstname, lastname, message FROM profile WHERE user_id=:id")
    result = db.session.execute(sql, {"id": users_id})
    user = result.fetchone()
    return user

def get_photo(users_id):
    """requesting photo info"""
    sql3 = text("SELECT file_name FROM photos WHERE user_id=:id ORDER BY id DESC")
    result3 = db.session.execute(sql3, {"id": users_id})
    photo = result3.fetchone()
    return photo

def insert_photo(users_id,name):
    """adding photo to database"""
    sql = text("""INSERT INTO photos (user_id, file_name)
            VALUES (:id, :filename) ON CONFLICT (user_id) 
            DO UPDATE SET file_name = EXCLUDED.file_name""")
    db.session.execute(sql, {"id": users_id, "filename": name})
    db.session.commit()

def get_contacts(users_id):
    """requesting contact info"""
    sql = text("""SELECT P.firstname, P.lastname, P.message, P.user_id,
                F.file_name FROM contact C JOIN profile P 
                ON C.contact_id = P.user_id LEFT JOIN photos F
                ON F.user_id=C.contact_id  WHERE C.user_id=:id""")
    result = db.session.execute(sql, {"id": users_id})

    contacts = result.fetchall()
    return contacts

def insert_contact(users_id,contact_id):
    """adding new contact to users contact list database"""
    sql = text("INSERT INTO contact (user_id, contact_id) VALUES (:id1, :id2)")
    db.session.execute(sql, {"id1": users_id, "id2": contact_id})
    db.session.commit()
