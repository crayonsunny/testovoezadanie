from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField, StringField, FileField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required

class LoginForm(Form):
    login = TextField('login', [validators.Length(max=48)])
    pswd = PasswordField('pswd', [validators.Length(min=6, max=35)])
    remember_me = BooleanField('remember_me', default = False)

class RegistrationForm(Form):
    login = TextField('login', [validators.Length(max=48)])
    email = EmailField('email', [validators.Length(min=6, max=70)])
    newpswd = PasswordField('newpswd', [
        validators.DataRequired(),
        validators.Length(min=6, max=35),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('confirm', validators = [Required()])
    accept_tos = BooleanField('I accept the TOS',
                              [validators.DataRequired(message='You have to accept the TOS')],
                              default = False)
    
class RenewalForm(Form):
    oldlogin = TextField('oldlogin', [
        validators.Length(max=48)
        ])
    renewlogin = TextField('renewlogin', [
        validators.optional(),
        validators.Length(max=48)
        ])
    renewemail = EmailField('renewemail', [
        validators.optional(),
        validators.Length(min=6, max=70)
        ])
    renewpswd = PasswordField('renewpswd', [
        validators.optional(),
        validators.Length(min=6, max=35),
        validators.EqualTo('renewconfirm', message='Please confirm the password')
        ])
    renewconfirm = PasswordField('confirm', [
        validators.optional(),
        validators.EqualTo('renewpswd', message='Please enter the password')
        ])

class DeleteForm(Form):
    login = TextField('login', [validators.Length(max=48)])
    pswd = PasswordField('pswd', [validators.Length(min=6, max=48)])

class IndexForm(Form):
    file = FileField('file')
