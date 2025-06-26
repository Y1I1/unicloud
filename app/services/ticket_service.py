from app import db
from app.models import Ticket

def create_ticket(form, user_id):
    ticket = Ticket()
    ticket.title = form.title.data
    ticket.description = form.description.data
    ticket.priority = form.priority.data
    ticket.status = form.status.data
    ticket.department_id = form.department_id.data
    ticket.user_id = user_id
    db.session.add(ticket)
    db.session.commit()
    return ticket

def update_ticket(ticket, form):
    ticket.title = form.title.data
    ticket.description = form.description.data
    ticket.priority = form.priority.data
    ticket.status = form.status.data
    ticket.department_id = form.department_id.data
    db.session.commit()
    return ticket

def close_ticket(ticket):
    ticket.status = 'Closed'
    db.session.commit()

def reopen_ticket(ticket):
    ticket.status = 'Open'
    db.session.commit()

def delete_ticket(ticket):
    db.session.delete(ticket)
    db.session.commit()

def delete_user_tickets(user):
    Ticket.query.filter_by(user_id=user.id).delete()
    db.session.commit() 