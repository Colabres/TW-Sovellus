"""
Routes Module

This module contains all the route definitions for the Flask application.
"""

from flask import render_template
from app import app
import login
import dialogue
import profiles
import register
import contactlist


@app.route('/')

def index():
    """loading start"""
    message=""
    return render_template('index.html', message=message)

@app.route('/process_form', methods=['POST'])
def process_form():
    """handling login"""
    return login.user_login()

@app.route('/register')
def register_info():
    """handling register"""
    message=""
    return render_template('register.html', message=message)

@app.route('/register_form', methods=['POST'])
def reg_form():
    """handling register form"""
    return register.register_form()

@app.route("/id<int:user_id>/send<int:receiver>")
def dial(user_id,receiver):
    """handling dialogue"""
    return dialogue.dialogue(user_id,receiver)

@app.route("/logout")
def logout():
    """handling logingout"""
    return login.logout()


@app.route("/send", methods=['POST'])
def send_message():
    """sending message"""
    return dialogue.send_message()


@app.route("/search", methods=['GET'])
def search():
    """searching for users"""
    return profiles.search()


@app.route("/profile<int:profile_id>")
def profile(profile_id):
    """looking at profile"""
    return profiles.profile(profile_id)


@app.route("/addcontact<int:contact_id>")
def addcontact(contact_id):
    """adding contact"""
    return contactlist.add_contact(contact_id)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    """editing profile"""
    return profiles.edit()


@app.route('/contactlist')
def get_contacts():
    """loading contactlist"""
    return contactlist.contactlist()


@app.route("/upload", methods=["POST"])
def upload_file():
    """uploading picture"""
    return profiles.upload()
