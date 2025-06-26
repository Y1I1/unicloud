from app import db
from app.models import User

def create_user(form):
    username = getattr(form, 'username', None)
    email = getattr(form, 'email', None)
    role = getattr(form, 'role', None)
    password = getattr(form, 'password', None)
    reset_password = getattr(form, 'reset_password', None)
    is_admin = getattr(form, 'is_admin', None)
    
    user = User()
    user.username = username.data if username else None
    user.email = email.data if email else None
    if role:
        user.role = role.data
    elif is_admin and is_admin.data:
        user.role = 'admin'
    else:
        user.role = 'regular'
    # For new users, password is required if provided
    if password and password.data:
        user.set_password(password.data)
    
    db.session.add(user)
    db.session.commit()
    return user

def update_user(user, form):
    username = getattr(form, 'username', None)
    email = getattr(form, 'email', None)
    role = getattr(form, 'role', None)
    password = getattr(form, 'password', None)
    reset_password = getattr(form, 'reset_password', None)
    
    if username:
        user.username = username.data
    if email:
        user.email = email.data
    if role:
        user.role = role.data
    # Only update password if reset_password is checked and password is provided
    if reset_password and reset_password.data and password and password.data:
        user.set_password(password.data)
    
    db.session.commit()
    return user

def promote_user(user):
    user.role = 'admin'
    db.session.commit()

def demote_user(user):
    user.role = 'regular'
    db.session.commit()

def delete_user(user):
    db.session.delete(user)
    db.session.commit() 