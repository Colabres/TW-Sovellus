
from flask import redirect, request, render_template, session, send_file, url_for, flash ,make_response,jsonify
from forms import EditProfileForm
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from sqlalchemy import text
from db import db
from werkzeug.datastructures import MultiDict
import re
import base64
import os


@app.route('/')
def index():
    message=""
    return render_template('index.html',message=message)


@app.route('/process_form', methods=['POST'])
def process_form():
    action = request.form.get('action')
    error_message=""
    if action == 'login':
        
        login = request.form.get('login')
        password = request.form.get('password')
        
        
        
        sql = text("SELECT id, password FROM users WHERE login=:login")
        result = db.session.execute(sql, {"login":login})
        user = result.fetchone()

        id = user.id    
        if not user:
            error_message="user dose not exist"
        else:
            hash_value = user.password
        if check_password_hash(hash_value, password):
            #session["login"] = login #?? do i still need it ?
            session["id"] = id
            #session["receiver"] = 6 #temporarry for testing purpuse
            receiver = session["receiver"]
            return redirect(f"/id{id}/send{receiver}") #need to change it to starting page then it will be ready
        else:
            error_message="invalid password"
        
        if error_message:
            return render_template('index.html',message=error_message)


@app.route('/register')
def register():
    message=""
    return render_template('register.html',message=message)

@app.route('/register_form', methods=['POST'])
def register_form():
    action = request.form.get('action')
    if action == 'register':
        # Handle registration logic
        def invalid_password(password):    
            pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).+$')
            return not bool(pattern.match(password))
        def invalid_username(login):
            sql = text("SELECT * FROM users WHERE login=:login")
            result = db.session.execute(sql, {"login":login})
            exists = bool(result.fetchone())
            return exists
        
        
        new_login = request.form.get('login')
        new_password = request.form.get('password')
        firstname    = request.form.get('firstname')
        lastname     = request.form.get('lastname')
        error_message= ""
        if len(new_login) < 5 :
            error_message="username is to short."
        elif invalid_username(new_login):
            error_message="username allready taken"
        elif len(new_password)< 5 :
            error_message="password is to short"
        elif invalid_password(new_password) :
            error_message="invalid password"

        if error_message:
            return render_template('register.html',message=error_message)
        else:
            hash_value = generate_password_hash(new_password)      
            sql = text("INSERT INTO users (login,password) VALUES (:login,:password)")
            db.session.execute(sql, {"login":new_login,"password":hash_value})
            db.session.commit()
            
            sql = text("SELECT id FROM users WHERE login=:login")
            result = db.session.execute(sql, {"login":new_login})
            user = result.fetchone()

            id = user.id


            sql = text("INSERT INTO profile (user_id,firstname,lastname) VALUES (:id,:firstname,:lastname)")
            db.session.execute(sql, {"id":id,"firstname":firstname,"lastname":lastname})
            db.session.commit()



            session["id"] = id
            session["receiver"] = 6
            receiver= session["receiver"]
            return redirect(f"/id{id}/send{receiver}")


@app.route("/id<int:id>/send<int:receiver>")
def home(id, receiver):
    if session["id"] == id:
        session["receiver"] = receiver
        

        sql = text("SELECT M.message,M.sender_id,P.firstname,P.lastname FROM message M JOIN profile P ON M.sender_id = P.user_id  WHERE sender_id=:id1 AND receiver_id=:id2 OR sender_id=:id3 AND receiver_id=:id4 ORDER BY M.id")
        result = db.session.execute(sql, {"id1": id,"id2": receiver,"id3":receiver,"id4":id})
        messages = result.fetchall()

        sql = text("SELECT M.message,M.sender_id,M.receiver_id,receiver.firstname AS receiver_firstname,receiver.lastname AS receiver_lastname,R.file_name AS receiver_photo,sender.firstname AS sender_firstname,sender.lastname AS sender_lastname,S.file_name AS sender_photo,M.id,P.user_id FROM message M JOIN profile P ON M.sender_id = P.user_id JOIN profile sender ON M.sender_id = sender.user_id JOIN profile receiver ON M.receiver_id = receiver.user_id JOIN photos R ON R.user_id = M.receiver_id JOIN photos S ON S.user_id = M.sender_id WHERE sender_id=:id1 OR receiver_id=:id1 ORDER BY M.id DESC")
        result2 = db.session.execute(sql, {"id1": id})
        contacts = result2.fetchall()

        new_contacts = []
        
        unique_user_pairs = set()
        for contact in contacts:
            
            contact_ids = tuple(sorted((contact.sender_id, contact.receiver_id)))
            
            
            if contact_ids not in unique_user_pairs:
                unique_user_pairs.add(contact_ids)
                new_contacts.append(contact)
                
        
        return render_template('dialogue.html', messages=messages,id=id,new_contacts=new_contacts,receiver=receiver)


@app.route("/logout")
def logout():
    del session["id"]
    return redirect("/")

@app.route("/send", methods=['POST'])
def send_message():
    message = request.form.get('message')
    id = session["id"]
    receiver = session["receiver"]
    if len(message)>0:
        sql = text("INSERT INTO message (sender_id,receiver_id,message) VALUES (:id1,:id2,:message)")
        db.session.execute(sql, {"id1":id,"id2":receiver,"message":message})
        db.session.commit()

    return redirect(f"/id{id}/send{receiver}")

@app.route("/search", methods=['GET'])
def search():
    name = request.args.get('search')

    sql = text("SELECT * FROM profile WHERE firstname=:name")
    result = db.session.execute(sql, {"name": name})
    users = result.fetchall()

    return render_template('searchresult.html', users = users)
    
@app.route("/profile<int:profile_id>")
def profile(profile_id):
        id=session["id"]
    #if session[id]==id:
        sql = text("SELECT firstname,lastname,message,user_id FROM profile WHERE user_id=:id")
        result = db.session.execute(sql, {"id": profile_id})
        user = result.fetchone()

        sql2 = text("SELECT contact_id FROM contact WHERE user_id=:id")
        result2 = db.session.execute(sql2, {"id":id})
        contact=result2.fetchone()

        sql3 = text("SELECT file_name FROM photos WHERE user_id=:id ORDER BY id DESC")
        result3 = db.session.execute(sql3, {"id":id})
        photo=result3.fetchone()
        if photo is not None:
            photo=photo[0]



        if user and user.firstname:
            firstname = user.firstname
        else: firstname = "Not"
        if user and user.lastname:
            lastname = user.lastname
        else: lastname = "Sure"
        if user and user.message:
            message =user.message
        else: message="Hi i am new around here!"
        if user and user.user_id:
            user_id =user.user_id
        else: user_id ="0"

        return render_template('profile.html',firstname=firstname,lastname=lastname,message=message,user_id=user_id,contact=contact,photo=photo)

@app.route("/addcontact<int:contact_id>")
def addcontact(contact_id):
    id = session["id"]
    sql = text("INSERT INTO contact (user_id,contact_id) VALUES (:id1,:id2)")
    db.session.execute(sql, {"id1":id,"id2":contact_id})
    db.session.commit()
    return redirect(f"/id{id}/send{contact_id}")



@app.route('/edit', methods=['GET', 'POST'])
def edit_profile(error=None):
    id = session['id'] 

    if request.method == 'POST':
 
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        message = request.form['message']
        
        sql = text("UPDATE profile SET firstname=:firstname, lastname=:lastname, message=:message WHERE user_id=:id")
        db.session.execute(sql, {"firstname": firstname, "lastname": lastname, "message": message, "id": id})
        db.session.commit()

        flash(f"Form submitted: First Name - {firstname}, Last Name - {lastname}, Message - {message}", 'success')
        return redirect(f"/profile{id}")

           
    sql = text("SELECT firstname,lastname,message FROM profile WHERE user_id=:id")
    result = db.session.execute(sql, {"id": id})
    user = result.fetchone()
    
    user_data = {
    'firstname': user[0], 
    'lastname': user[1],   
    'message': user[2] if user[2] is not None else 'hi',  # handle None values
    }
    user_data_multidict = MultiDict(user_data)

    form = EditProfileForm(formdata=user_data_multidict)

    return render_template('editprofile.html', form=form)

@app.route('/contactlist')
def contactlist():
    id = session["id"]

    sql = text("SELECT P.firstname,P.lastname,P.message,P.user_id FROM contact C JOIN profile P ON C.contact_id = P.user_id  WHERE C.user_id=:id")
    result = db.session.execute(sql, {"id":id})   

    contacts=result.fetchall()

    return render_template("contacts.html", contacts=contacts)



@app.route("/upload", methods=["POST"])
def upload_file():
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
    name=str(id)+file.filename
    file_path = os.path.join(upload_folder, name )
    file.save(file_path)

    
    sql = text("INSERT INTO photos (user_id,file_name) VALUES (:id,:filename)")
    db.session.execute(sql, {"id":id,"filename":name})
    db.session.commit()    
    
    return redirect(f"/edit")