

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class EditProfileForm(FlaskForm):
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    message = StringField('Message')
    submit = SubmitField('Save Changes')

