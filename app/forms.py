from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User, Department
import re


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=32, message='Username must be between 3 and 32 characters')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=32, message='Username must be between 3 and 32 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email must be less than 120 characters')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    is_admin = BooleanField('Register as Admin')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        original_username = getattr(self, 'original_username', None)
        if original_username:
            # Editing existing user
            current_user_obj = User.query.filter_by(username=original_username).first()
            if current_user_obj and email.data == current_user_obj.email:
                return  # Email unchanged, skip uniqueness check
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email address.')

    def validate_password(self, password):
        pw = password.data or ''
        if not re.search(r'[A-Z]', pw):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'\d', pw):
            raise ValidationError('Password must contain at least one number.')
        if not re.search(r'[^A-Za-z0-9]', pw):
            raise ValidationError('Password must contain at least one special character.')


class TicketForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(message='Title is required'),
        Length(min=5, max=100, message='Title must be between 5 and 100 characters')
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(message='Description is required'),
        Length(min=10, max=1000, message='Description must be between 10 and 1000 characters')
    ])
    department_id = SelectField('Department', coerce=int, validators=[
        DataRequired(message='Department is required')
    ])
    priority = SelectField('Priority', choices=[
        ('Low', 'Low'),
        ('Normal', 'Normal'),
        ('High', 'High')
    ], validators=[DataRequired(message='Priority is required')])
    status = SelectField('Status', choices=[
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed')
    ], validators=[DataRequired(message='Status is required')])
    submit = SubmitField('Submit Ticket')

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.department_id.choices = [(d.id, d.name) for d in Department.query.order_by('name').all()]


class DepartmentForm(FlaskForm):
    name = StringField('Department Name', validators=[
        DataRequired(message='Department name is required'),
        Length(min=2, max=50, message='Department name must be between 2 and 50 characters')
    ])
    submit = SubmitField('Save Department')


class UserForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=32, message='Username must be between 3 and 32 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email must be less than 120 characters')
    ])
    reset_password = BooleanField('Reset Password')
    password = PasswordField('New Password')
    password2 = PasswordField('Repeat Password')
    role = SelectField('Role', choices=[
        ('regular', 'Regular User'),
        ('admin', 'Admin')
    ], validators=[DataRequired(message='Role is required')])
    submit = SubmitField('Save User')

    def __init__(self, original_username=None, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        original_username = getattr(self, 'original_username', None)
        if original_username:
            # Editing existing user
            current_user_obj = User.query.filter_by(username=original_username).first()
            if current_user_obj and email.data == current_user_obj.email:
                return  # Email unchanged, skip uniqueness check
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email address.')
    
    def validate_password(self, password):
        pw = password.data or ''
        # Only validate password if reset_password is checked
        if self.reset_password.data:
            if not pw:
                raise ValidationError('Password is required when resetting password.')
            if len(pw) < 8:
                raise ValidationError('Password must be at least 8 characters long')
            if not re.search(r'[A-Z]', pw):
                raise ValidationError('Password must contain at least one uppercase letter.')
            if not re.search(r'\d', pw):
                raise ValidationError('Password must contain at least one number.')
            if not re.search(r'[^A-Za-z0-9]', pw):
                raise ValidationError('Password must contain at least one special character.')

    def validate_password2(self, password2):
        # Only validate password2 if reset_password is checked
        if self.reset_password.data:
            if not password2.data:
                raise ValidationError('Please repeat the password.')
            if password2.data != self.password.data:
                raise ValidationError('Passwords must match') 