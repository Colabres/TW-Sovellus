from flask import session,render_template,redirect
import db

def contactlist():
    id = session["id"]

    contacts=db.get_contacts(id)

    return render_template("contacts.html", contacts=contacts)

def add_contact(contact_id):
    
    id = session["id"]
    db.insert_contact(id,contact_id)

    return redirect(f"/id{id}/send{contact_id}")
