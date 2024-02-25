""" profile module """
import os
from flask import session,render_template,request,redirect,jsonify
from werkzeug.datastructures import MultiDict
from forms import EditProfileForm
import db


def profile(profile_id):
    """loading profile"""
    info=db.request_profile(profile_id)
    user=info[0]
    contact=info[1]


    if info[2] is not None:
        photo = info[2][0]
    else:
        photo = None

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

def edit():
    """editing profile"""
    users_id = session['id']

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        message = request.form['message']

        db.update_profile(users_id,firstname,lastname,message)

        return redirect(f"/profile{users_id}")

    user=db.request_profile_info(users_id)

    user_data = {
        'firstname': user[0],
        'lastname': user[1],
        'message': user[2] if user[2] is not None else 'hi',  # handle None values
    }
    user_data_multidict = MultiDict(user_data)

    form = EditProfileForm(formdata=user_data_multidict)

    photo=db.get_photo(users_id)
    if photo is not None:
        photo = photo[0]

    return render_template('editprofile.html', form=form, photo=photo)

def search():
    """seraching for users"""
    name = request.args.get('search')
    users = db.search_request(name)
    return render_template('searchresult.html', users=users)

def upload():
    """upload photo file"""
    users_id = session["id"]
    # check if the post request has the file part

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # save the file to a folder
    upload_folder = 'static/uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    name = str(users_id) + file.filename
    file_path = os.path.join(upload_folder, name)
    file.save(file_path)


    db.insert_photo(users_id,name)

    return redirect("/edit")
