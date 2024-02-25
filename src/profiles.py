from flask import session,render_template,request,redirect,jsonify
from werkzeug.datastructures import MultiDict
from forms import EditProfileForm
import db
import os

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

def edit():
    
    id = session['id']

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        message = request.form['message']

        db.update_profile(id,firstname,lastname,message)

        return redirect(f"/profile{id}")

    user=db.request_profile_info(id)

    user_data = {
        'firstname': user[0],
        'lastname': user[1],  
        'message': user[2] if user[2] is not None else 'hi',  # handle None values
    }
    user_data_multidict = MultiDict(user_data)

    form = EditProfileForm(formdata=user_data_multidict)

    photo=db.get_photo(id)
    if photo is not None:
        photo = photo[0]

    return render_template('editprofile.html', form=form, photo=photo)

def search():
    name = request.args.get('search')
    users = db.search_request(name)
    return render_template('searchresult.html', users=users)

def upload():    
    id = session["id"]
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
    name = str(id) + file.filename
    file_path = os.path.join(upload_folder, name)
    file.save(file_path)


    db.insert_photo(id,name)

    return redirect(f"/edit")