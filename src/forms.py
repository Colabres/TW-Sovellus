"""form module"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class EditProfileForm(FlaskForm):
    """class for filing in the form"""
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    message = StringField('Message')
    submit = SubmitField('Save Changes')
