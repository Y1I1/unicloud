print('Starting seed.py')

from app import create_app, db
from app.models import User, Ticket, Department

def seed_data():
    try:
        app = create_app()
        with app.app_context():
            print('Dropping and creating all tables...')
            db.drop_all()
            db.create_all()
            print('Tables created.')

            # Create Admin User
            admin_user = User()
            admin_user.username = 'admin'
            admin_user.email = 'admin@example.com'
            admin_user.role = 'admin'
            admin_user.set_password('P@ssword1')
            db.session.add(admin_user)
            print('Admin user created.')

            # Create 10 Regular Users (user1 uses P@ssword1)
            for i in range(1, 11):
                user = User()
                user.username = f'user{i}'
                user.email = f'user{i}@example.com'
                user.role = 'regular'
                if i == 1:
                    user.set_password('P@ssword1')
                else:
                    user.set_password(f'Password{i}!')
                db.session.add(user)
            print('Regular users created.')
            db.session.commit()

            # Create 10 Departments
            departments = [
                'IT Support', 'Human Resources', 'Finance', 'Marketing', 'Sales',
                'Operations', 'Customer Service', 'R&D', 'Legal', 'Facilities'
            ]
            for i, dept_name in enumerate(departments, 1):
                dept = Department()
                dept.name = dept_name
                db.session.add(dept)
            print('Departments created.')
            db.session.commit()

            # Create 10 Tickets (variety of priorities, statuses, and assignments)
            users = User.query.filter(User.role == 'regular').all()
            departments = Department.query.all()
            ticket_data = [
                ('System Login Issue', 'Cannot access email system', 'High', 'Open'),
                ('Printer Not Working', 'Printer shows offline status', 'Normal', 'Open'),
                ('Software Installation', 'Need Adobe Creative Suite installed', 'Low', 'In Progress'),
                ('Network Connectivity', 'WiFi connection unstable', 'High', 'Open'),
                ('Password Reset', 'Forgot password for database access', 'Normal', 'Closed'),
                ('Hardware Replacement', 'Laptop keyboard malfunctioning', 'High', 'Open'),
                ('Software Update', 'Windows update causing issues', 'Normal', 'In Progress'),
                ('Email Configuration', 'Outlook not syncing properly', 'Low', 'Open'),
                ('VPN Access', 'Cannot connect to company VPN', 'High', 'Closed'),
                ('Backup Request', 'Need data backup for project files', 'Normal', 'Open')
            ]
            for i, (title, description, priority, status) in enumerate(ticket_data):
                ticket = Ticket()
                ticket.title = title
                ticket.description = description
                ticket.priority = priority
                ticket.status = status
                ticket.user_id = users[i % len(users)].id
                ticket.department_id = departments[i % len(departments)].id
                db.session.add(ticket)
            print('Tickets created.')
            db.session.commit()

            # Verify record counts
            user_count = User.query.count()
            dept_count = Department.query.count()
            ticket_count = Ticket.query.count()

            print(f"\nDatabase has been seeded with initial help desk data:")
            print(f"- Users: {user_count} (including 1 admin, 10 regular)")
            print(f"- Departments: {dept_count}")
            print(f"- Tickets: {ticket_count}")
            print("\nLogin credentials for testing:")
            print("Admin:    username=admin    password=P@ssword1")
            print("User:     username=user1    password=P@ssword1")
            print("\nYou can now log in and test both admin and regular accounts.")
    except Exception as e:
        print(f'Error during seeding: {e}')

if __name__ == '__main__':
    seed_data() 