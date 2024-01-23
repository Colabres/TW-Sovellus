
from flask import Flask
from flask_bootstrap import Bootstrap
from db import db
from os import getenv



app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://"
app.secret_key = getenv("SECRET_KEY")
app.config['WTF_CSRF_ENABLED'] = True

db.init_app(app)



    


import routes