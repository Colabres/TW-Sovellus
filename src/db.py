from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

def login_request(login):
    sql = text("SELECT id, password FROM users WHERE login=:login")
    result = db.session.execute(sql, {"login":login})
    user = result.fetchone()
    
    return user
