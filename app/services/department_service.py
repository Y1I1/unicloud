from app import db
from app.models import Department


def create_department(form):
    if not hasattr(form, 'name') or not hasattr(form.name, 'data'):
        raise TypeError('create_department expects a DepartmentForm with a .name.data attribute')
    department = Department()
    department.name = form.name.data
    db.session.add(department)
    db.session.commit()
    return department


def update_department(department, form):
    if not hasattr(form, 'name') or not hasattr(form.name, 'data'):
        raise TypeError('update_department expects a DepartmentForm with a .name.data attribute')
    department.name = form.name.data
    db.session.commit()
    return department


def delete_department(department):
    db.session.delete(department)
    db.session.commit() 