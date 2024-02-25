"""dialogue module"""
from flask import session,render_template,redirect,request
import db

def dialogue(users_id, receiver):
    """loading dialogue"""
    if session["id"] == users_id:
        session["receiver"] = receiver
        request_result=db.dialogue_request(users_id,receiver)
        contacts=request_result[1]
        messages=request_result[0]

        new_contacts = []
        unique_user_pairs = set()
        for contact in contacts:
            contact_ids = tuple(sorted((contact.sender_id, contact.receiver_id)))
            if contact_ids not in unique_user_pairs:
                unique_user_pairs.add(contact_ids)
                new_contacts.append(contact)
        return render_template('dialogue.html', messages=messages,
                                id=users_id, new_contacts=new_contacts, receiver=receiver)

    return redirect(f"/id{users_id}/send{receiver}")

def send_message():
    """sending message"""
    message = request.form.get('message')
    users_id = session["id"]
    receiver = session["receiver"]
    if len(message) > 0:
        db.insert_message(users_id,receiver,message)
    return redirect(f"/id{users_id}/send{receiver}")
