from flask import session,render_template,request
import db

def profile(profile_id):
    
    info=db.request_profile(profile_id)
    user=info[0]
    contact=info[1]


    if info[2] is not None:
        photo = info[2][0]

    if user and user.firstname:
        firstname = user.firstname
    else:
        firstname = "Not"
    if user and user.lastname:
        lastname = user.lastname
    else:
        lastname = "Sure"
    if user and user.message:
        message = user.message
    else:
        message = "Hi i am new around here!"
    if user and user.user_id:
        user_id = user.user_id
    else:
        user_id = "0"

    return render_template('profile.html',firstname=firstname,
                           lastname=lastname,message=message,
                           user_id=user_id, contact=contact, photo=photo)

def search():
    name = request.args.get('search')

    users = db.search_request(name)


    return render_template('searchresult.html', users=users)