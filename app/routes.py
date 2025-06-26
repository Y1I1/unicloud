from flask import render_template, flash, redirect, url_for, request, jsonify, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Ticket, Department
from app.forms import LoginForm, RegistrationForm, TicketForm, DepartmentForm, UserForm
from urllib.parse import urlsplit
from functools import wraps
import logging
from flask_paginate import Pagination, get_page_parameter
from app.services import user_service
from app.services import ticket_service, department_service
from app import db
from datetime import datetime

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Create main blueprint
main_bp = Blueprint('main', __name__)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('This page is for admins only.', 'danger')
            return redirect(url_for('main.index'))
        return fn(*args, **kwargs)
    return wrapper

@main_bp.route('/')
@main_bp.route('/index')
@login_required
def index():
    search = request.args.get('search', '').strip()
    status_filter = request.args.get('status', 'open').lower()  # 'open' or 'closed'
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Build base query
    if current_user.role == 'admin':
        query = Ticket.query
    else:
        query = Ticket.query.filter_by(user_id=current_user.id)

    # Apply search
    if search:
        query = query.filter(
            (Ticket.title.ilike(f'%{search}%')) |
            (Ticket.description.ilike(f'%{search}%'))
        )

    # Apply status filter
    if status_filter == 'closed':
        query = query.filter(Ticket.status == 'Closed')
    else:
        query = query.filter(Ticket.status != 'Closed')

    tickets = query.order_by(Ticket.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    # Stats for summary cards
    total_tickets = Ticket.query.count() if current_user.role == 'admin' else Ticket.query.filter_by(user_id=current_user.id).count()
    pending_tickets = Ticket.query.filter_by(status='Open').count() if current_user.role == 'admin' else Ticket.query.filter_by(user_id=current_user.id, status='Open').count()
    closed_tickets = Ticket.query.filter_by(status='Closed').count() if current_user.role == 'admin' else Ticket.query.filter_by(user_id=current_user.id, status='Closed').count()
    stats = {
        'total': total_tickets,
        'pending': pending_tickets,
        'closed': closed_tickets
    }
    return render_template('index.html', title='Dashboard', tickets=tickets.items, pagination=tickets, stats=stats, search=search, status_filter=status_filter)

@main_bp.route('/create_ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = TicketForm()
    form.department_id.choices = [(d.id, d.name) for d in Department.query.order_by(Department.name).all()]
    if form.validate_on_submit():
        ticket = ticket_service.create_ticket(form, current_user.id)
        flash('Your ticket has been created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('ticket_form.html', title='New Ticket', form=form, ticket=None, departments=Department.query.all())

@main_bp.route('/ticket/<int:ticket_id>')
@login_required
def ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if current_user.role != 'admin' and ticket.user != current_user:
        flash('You do not have permission to view this ticket.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('ticket_detail.html', title=ticket.title, ticket=ticket)

@main_bp.route('/edit_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if current_user.role != 'admin' and ticket.user != current_user:
        flash('You do not have permission to edit this ticket.', 'danger')
        return redirect(url_for('main.index'))
    form = TicketForm(obj=ticket)
    form.department_id.choices = [(d.id, d.name) for d in Department.query.order_by(Department.name).all()]
    if form.validate_on_submit():
        ticket = ticket_service.update_ticket(ticket, form)
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('main.ticket', ticket_id=ticket.id))
    elif request.method == 'GET':
        form.title.data = ticket.title
        form.description.data = ticket.description
        form.department_id.data = ticket.department_id
        form.priority.data = ticket.priority
        form.status.data = ticket.status
    return render_template('ticket_form.html', title='Edit Ticket', form=form, ticket=ticket, departments=Department.query.all())

@main_bp.route('/ticket/<int:ticket_id>/close', methods=['POST'])
@login_required
@admin_required
def close_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket_service.close_ticket(ticket)
    flash('Ticket has been closed.', 'success')
    return redirect(url_for('main.ticket', ticket_id=ticket.id))

@main_bp.route('/ticket/<int:ticket_id>/reopen', methods=['POST'])
@login_required
@admin_required
def reopen_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket_service.reopen_ticket(ticket)
    flash('Ticket has been reopened.', 'success')
    return redirect(url_for('main.ticket', ticket_id=ticket.id))

@main_bp.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
@login_required
@admin_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket_service.delete_ticket(ticket)
    flash('The ticket has been deleted.', 'success')
    return redirect(url_for('main.index'))

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard showing system statistics"""
    total_users = User.query.count()
    total_tickets = Ticket.query.count()
    open_tickets = Ticket.query.filter_by(status='Open').count()
    total_departments = Department.query.count()
    
    stats = {
        'total_users': total_users,
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'total_departments': total_departments
    }
    return render_template('admin_dashboard.html', stats=stats)

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    search = request.args.get('search', '')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    query = User.query
    if search:
        query = query.filter(User.username.ilike(f'%{search}%'))
    users = query.order_by(User.id).paginate(page=page, per_page=per_page, error_out=False)
    pagination = Pagination(page=page, total=users.total, search=search, record_name='users', per_page=per_page)
    return render_template('admin_users.html', users=users.items, pagination=pagination, search=search, aria_label_users="User list")

@admin_bp.route('/promote/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def promote_user(user_id):
    user = User.query.get_or_404(user_id)
    user_service.promote_user(user)
    flash(f'{user.username} has been promoted to Admin.', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/demote/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def demote_user(user_id):
    user = User.query.get_or_404(user_id)
    user_service.demote_user(user)
    flash(f'{user.username} has been demoted to Regular User.', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.manage_users'))
    # Reassign tickets before deleting user, or handle as needed
    ticket_service.delete_user_tickets(user)
    user_service.delete_user(user)
    flash(f'User {user.username} has been deleted.', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/departments')
@login_required
@admin_required
def manage_departments():
    departments = Department.query.all()
    return render_template('admin_departments.html', title='Manage Departments', departments=departments)

@admin_bp.route('/add_department', methods=['GET', 'POST'])
@login_required
@admin_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        department = department_service.create_department(form)
        flash('The department has been added.', 'success')
        return redirect(url_for('admin.manage_departments'))
    return render_template('department_form.html', title='Add Department', form=form, department=None)

@admin_bp.route('/edit_department/<int:department_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_department(department_id):
    department = Department.query.get_or_404(department_id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department = department_service.update_department(department, form)
        flash('The department has been updated.', 'success')
        return redirect(url_for('admin.manage_departments'))
    elif request.method == 'GET':
        form.name.data = department.name
    return render_template('department_form.html', title='Edit Department', form=form, department=department)

@admin_bp.route('/delete_department/<int:department_id>', methods=['POST'])
@login_required
@admin_required
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)
    if department.tickets.first():
        flash('Cannot delete a department with active tickets. Please reassign tickets first.', 'warning')
        return redirect(url_for('admin.manage_departments'))
    department_service.delete_department(department)
    flash('The department has been deleted.', 'success')
    return redirect(url_for('admin.manage_departments'))

@main_bp.route('/explore/users')
@login_required
def explore_users():
    search = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    query = User.query
    if search:
        query = query.filter(User.username.ilike(f'%{search}%'))
    users = query.order_by(User.id).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('explore_users.html', title='Explore Users', users=users.items, pagination=users, search=search)

@main_bp.route('/explore/departments')
@login_required
def explore_departments():
    departments = Department.query.all()
    return render_template('explore_departments.html', title='Explore Departments', departments=departments)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('main.login'))
        
        # Check if account is locked
        if user.is_locked():
            flash('Account is temporarily locked due to multiple failed login attempts. Please try again later.', 'danger')
            return redirect(url_for('main.login'))
        
        if not user.check_password(form.password.data):
            user.record_failed_login()
            flash('Invalid username or password', 'danger')
            return redirect(url_for('main.login'))
        
        # Successful login
        user.reset_failed_attempts()
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
        return redirect(next_page)
    elif request.method == 'POST':
        # Form validation failed
        flash('Invalid username or password', 'error')
    
    return render_template('login.html', title='Sign In', form=form)

@main_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = user_service.create_user(form)
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@admin_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = user_service.create_user(form)
        flash(f'User {user.username} has been created.', 'success')
        return redirect(url_for('admin.manage_users'))
    return render_template('user_form.html', title='Add User', form=form)

@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(original_username=user.username)
    if request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.role.data = user.role
        form.reset_password.data = False  # Always start unchecked
    if form.validate_on_submit():
        changed = False
        if form.username.data != user.username:
            user.username = form.username.data
            changed = True
        if form.email.data != user.email:
            user.email = form.email.data
            changed = True
        if form.role.data != user.role:
            user.role = form.role.data
            changed = True
        if form.reset_password.data and form.password.data:
            user.set_password(form.password.data)
            changed = True
        if changed:
            db.session.commit()
            flash(f'User {user.username} has been updated.', 'success')
        else:
            flash(f'No changes were made to user {user.username}.', 'info')
        return redirect(url_for('admin.manage_users', page=1, search=''))
    elif request.method == 'POST':
        flash('There was a problem with your submission. Please check the form for errors.', 'danger')
    return render_template('user_form.html', title='Edit User', form=form, user=user)

@main_bp.route('/api/users')
@login_required
@admin_required
def api_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    } for user in users])

@main_bp.route('/user/<int:user_id>')
@login_required
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    tickets = None
    if current_user.role == 'admin' or current_user.id == user.id:
        tickets = user.tickets.order_by(Ticket.created_at.desc()).all()
    return render_template('user_profile.html', user=user, tickets=tickets)

print("routes.py loaded successfully") 
