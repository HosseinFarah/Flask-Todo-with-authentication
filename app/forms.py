from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, TextAreaField, SelectField,DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileRequired
from app import db 
from app.models import User, Todo
import re

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    phone=StringField('Phone Number', validators=[DataRequired()])
    address=StringField('Address', validators=[DataRequired()])
    zipcode=StringField('Zip Code', validators=[DataRequired()])
    image = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
    firstname_pattern = r"^[a-zåäöA-ZÅÄÖ'\-]+$"
    def validate_firstname(self, firstname):
        if not re.match(self.firstname_pattern, firstname.data):
            raise ValidationError('Invalid first name, please use only letters or hyphens or apostrophes.')
    
    def validate_lastname(self, lastname):
        if not re.match(self.firstname_pattern, lastname.data):
            raise ValidationError('Invalid last name, please use only letters or hyphens or apostrophes.')
    
    phone_pattern = r"^[0-9]{7,15}$"
    def validate_phone(self, phone):
        if not re.match(self.phone_pattern, phone.data):
            raise ValidationError('Invalid phone number, please use only numbers and between 7-15 characters.')
        user = User.query.filter_by(phone=phone.data).first()
        if user is not None:
            raise ValidationError('Please use a different phone number.')
    
    address_pattern = r"^[a-zåäöA-ZÅÄÖ0-9'\- ]+$"
    def validate_address(self, address):
        if not re.match(self.address_pattern, address.data):
            raise ValidationError('Invalid address, please use only letters, numbers, hyphens or apostrophes.')
    
    zipcode_pattern = r"^[0-9]{5}$"
    def validate_zipcode(self, zipcode):
        if not re.match(self.zipcode_pattern, zipcode.data):
            raise ValidationError('Invalid zip code, please use only numbers and 5 characters.')
        
class EditProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    address=StringField('Address', validators=[DataRequired()])
    zipcode=StringField('Zip Code', validators=[DataRequired()])
    image = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    submit = SubmitField('Update')
    
    firstname_pattern = r"^[a-zåäöA-ZÅÄÖ'\-]+$"
    def validate_firstname(self, firstname):
        if not re.match(self.firstname_pattern, firstname.data):
            raise ValidationError('Invalid first name, please use only letters or hyphens or apostrophes.')
    
    def validate_lastname(self, lastname):
        if not re.match(self.firstname_pattern, lastname.data):
            raise ValidationError('Invalid last name, please use only letters or hyphens or apostrophes.')
        
    address_pattern = r"^[a-zåäöA-ZÅÄÖ0-9'\- ]+$"
    def validate_address(self, address):
        if not re.match(self.address_pattern, address.data):
            raise ValidationError('Invalid address, please use only letters, numbers, hyphens or apostrophes.')
        
    zipcode_pattern = r"^[0-9]{5}$"
    def validate_zipcode(self, zipcode):
        if not re.match(self.zipcode_pattern, zipcode.data):
            raise ValidationError('Invalid zip code, please use only numbers and 5 characters.')
    


class AddTodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"rows": 5, "cols": 40})
    status = SelectField('Status', choices=[('pending', 'Pending'), ('completed', 'Completed'), ('in-progress', 'In-Progress')], validators=[DataRequired()],default='pending')
    date_todo = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add')
    
    status_pattern = r"^(pending|completed|in-progress)$"
    def validate_status(self, status):
        if not re.match(self.status_pattern, status.data):
            raise ValidationError('Invalid status, please use only "pending", "completed" or "in-progress".')
    
    title_pattern = r"^[a-zåäöA-ZÅÄÖ0-9'\- ]+$"
    def validate_title(self, title):
        if not re.match(self.title_pattern, title.data):
            raise ValidationError('Invalid title, please use only letters, numbers, hyphens or apostrophes.')
        
    description_pattern = r"^[a-zåäöA-ZÅÄÖ0-9 '\-.,():!\"*%?_\+\s]+$"
    def validate_description(self, description):
        if not re.match(self.description_pattern, description.data):
            raise ValidationError('Invalid description, please use only letters, numbers, hyphens, apostrophes, periods, commas, colons, parentheses, exclamation marks, quotation marks, asterisks, percentage signs, question marks, underscores, plus signs or spaces.')

class EditTodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[('pending', 'Pending'), ('completed', 'Completed'), ('in-progress', 'In-Progress')], validators=[DataRequired()],default='pending')
    date_todo = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Update')
    
    status_pattern = r"^(pending|completed|in-progress)$"
    def validate_status(self, status):
        if not re.match(self.status_pattern, status.data):
            raise ValidationError('Invalid status, please use only "pending", "completed" or "in-progress".')
    
    title_pattern = r"^[a-zåäöA-ZÅÄÖ0-9'\- ]+$"
    def validate_title(self, title):
        if not re.match(self.title_pattern, title.data):
            raise ValidationError('Invalid title, please use only letters, numbers, hyphens or apostrophes.')
        
    description_pattern = r"^[a-zåäöA-ZÅÄÖ0-9 '\-.,():!\"*%?_\+\s]+$"
    def validate_description(self, description):
        if not re.match(self.description_pattern, description.data):
            raise ValidationError('Invalid description, please use only letters, numbers, hyphens, apostrophes, periods, commas, colons, parentheses, exclamation marks, quotation marks, asterisks, percentage signs, question marks, underscores, plus signs or spaces.')
  