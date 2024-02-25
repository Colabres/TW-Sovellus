"""contactlist module"""
from flask import session,render_template,redirect
import db

def contactlist():
    """load contactlist"""
    users_id = session["id"]

    contacts=db.get_contacts(users_id)

    return render_template("contacts.html", contacts=contacts)

def add_contact(contact_id):
    """add new contact"""
    users_id = session["id"]
    db.insert_contact(users_id,contact_id)

    return redirect(f"/id{users_id}/send{contact_id}")
