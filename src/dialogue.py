from flask import session,render_template,redirect,request
import db

def dialogue(id, receiver):
    if session["id"] == id:
        session["receiver"] = receiver
        request_result=db.dialogue_request(id,receiver)
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
                                id=id, new_contacts=new_contacts, receiver=receiver)
    
def send_message():
    message = request.form.get('message')
    id = session["id"]
    receiver = session["receiver"]
    if len(message) > 0:
        db.insert_message(id,receiver,message)
    return redirect(f"/id{id}/send{receiver}")