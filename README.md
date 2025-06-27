Help Desk Ticketing System
This project is a Python web application that provides a simple help desk ticketing system for a small organization. It was developed as part of a Level 5 Software Engineering & Agile coursework to demonstrate a full-stack web application with role-based access. The system allows users to submit support tickets and administrators to manage those tickets, addressing the problem of tracking and resolving internal support requests efficiently. The scope of the application covers basic ticket management features (creation, updates, status tracking) and user management within a controlled, secure environment. The application focuses on modularity, security, and usability. It follows best practices such as a modular project structure, secure coding (including input validation and password hashing), user role validation for access control, and user-friendly features like flash notifications and confirmation prompts for destructive actions. This ensures that the system is maintainable and safe, providing a good foundation for learning agile development principles in a web project.
Technology Stack and Dependencies
Programming Language & Framework: Python 3 with the Flask web framework (utilizing Flask Blueprints for modular structure).
Database: SQLite (via Flask-SQLAlchemy ORM) for relational data storage, with a small schema (~3 tables for Users, Tickets, Departments) and initial seed data.
Authentication & Authorization: Flask-Login for session management and user authentication, supporting Admin and Regular user roles.
Form Handling & Validation: WTForms (Flask-WTF) for form generation and validation of user input (e.g., enforcing strong password rules and valid email format)
GitHub
.
Security: Passwords are hashed using Werkzeug security utilities; CSRF protection is enabled for forms; the app implements account lockout after multiple failed login attempts
GitHub
; and Flask-Limiter can be used to rate-limit requests (to prevent abuse).
Frontend: HTML5/Jinja2 templates styled with Bootstrap 5 for a responsive UI, plus FontAwesome for icons. Flash messages are used for user notifications (e.g., success or error alerts).
Miscellaneous: Flask-Migrate for database migrations, Gunicorn as a WSGI server for deployment, and Sentry SDK (optional) for error monitoring. All key dependencies are listed in requirements.txt
GitHub
.
Features and Best Practices
Modular Design: The code is organized using Blueprints and service modules, separating concerns for main user functionality and admin functionality. This makes the project easier to maintain and extend.
Role-Based Access Control: Two user roles are defined – Admin and Regular User. Admin pages and actions are protected so that only administrators can access them. For example, an @admin_required decorator restricts admin routes, redirecting non-admin users with an error message.
Secure Authentication & Validation: User credentials are stored securely (hashed passwords) and login attempts are monitored. The system locks an account for a period after too many failed logins to prevent brute-force attacks. All forms include validation rules (e.g., required fields, length limits, email format) and CSRF tokens for security.
CRUD Functionality: Administrators have full Create, Read, Update, Delete (CRUD) capabilities on core entities (tickets, user accounts, departments). Regular users have restricted CRUD – they can Create new tickets, Read and Update their own submissions, but cannot delete tickets or access other users’ data.
User Notifications: The interface provides feedback for actions using flash messages. Successful operations (e.g., ticket created, profile updated) show success notifications, whereas errors or permission denials show descriptive error alerts. This helps users understand the outcome of their actions.
Confirmation Prompts: Destructive actions require confirmation to prevent accidental changes. For instance, when an admin attempts to delete a record (such as a department or a user), a JavaScript confirmation dialog asks the user to confirm the deletion
GitHub
. This adds a safety net against accidental data loss.
Setup and Installation
Follow these steps to set up and run the application on your local machine:
Clone the Repository: Download or clone this project to your local environment using git clone <repository_url> (or download the ZIP and extract it).
Python Environment: Ensure you have Python 3.x installed. It’s recommended to create a virtual environment to isolate project dependencies:
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install Dependencies: Install the required Python packages using pip:
bash
Copy
Edit
pip install -r requirements.txt
This will install Flask and all other libraries the app depends on.
Configure Environment (Optional): By default, the app uses a SQLite database (app.db) in the project directory and a default secret key. You can adjust configurations in config.py if needed (e.g., provide a different SECRET_KEY or database URI via environment variables), but no action is required for a default setup.
Initialize the Database: Set up the database and seed it with initial data:
bash
Copy
Edit
python seed.py
This will create the database file and populate it with some sample records, including an admin user and some regular users, departments, and tickets for testing.
Run the Application: Start the Flask web server:
bash
Copy
Edit
python app.py
The app will launch on http://localhost:5000 (by default). You should see console output indicating the server is running. If running on a server or VM, the app is configured to host on 0.0.0.0 so it may be accessible via your network IP on port 5000.
Access the App: Open a web browser and navigate to http://localhost:5000. You should reach the login page of the Help Desk system. Use the sample credentials below (or register a new account) to log in and start using the application.
Sample Login Credentials
For convenience, you can use the following test accounts to explore the application:
Admin Account:
Username/Email: admin@example.com
Password: Admin@123
Regular User Account:
Username/Email: user@example.com
Password: User@123
Note: The admin account has full privileges, while the regular user account has limited access. You can also register a new user through the app's registration page. If you register a new account and mark "Register as Admin," that account will be created with administrator rights.
Basic Usage Guide
Once the application is running and you are logged in, the interface will differ based on your user role. Below is a guide to the main features available to each type of user:
Administrator Users: (full system access)
Dashboard & Ticket Management: After logging in, admins land on a dashboard showing an overview of all support tickets (with statistics like total open/closed tickets). Administrators can view all tickets submitted in the system, use search and filters, and click any ticket to see details. They can create new tickets (e.g., on behalf of users or test issues), edit/update any ticket, and change ticket statuses (e.g., mark as "Closed" when resolved). They also have options to close or reopen tickets, and can delete a ticket if needed (e.g., in case of spam or error).
User Management: Admins can view the list of all users and have the ability to add new users via a form, edit existing user details (including changing roles or resetting passwords), and deactivate or delete users. The system prevents deletion of the admin’s own account and ensures that when a user is deleted, their associated tickets are handled appropriately (tickets can be reassigned or removed as per business rules).
Department Management: Admins can create and manage departments (categories for tickets). They can add new departments or rename existing ones. If a department has active tickets associated with it, the system will prevent its deletion to avoid orphaned tickets (the admin would need to reassign or resolve those tickets first). All these management pages are accessible via the admin sidebar (e.g., Manage Users, Manage Departments sections).
Notifications & Prompts: Admin actions trigger flash notifications (e.g., “User X has been updated” or “Ticket closed successfully”) to confirm outcomes. Any irreversible actions like deletions will prompt for confirmation, ensuring the admin intentionally wants to proceed with the change.
Regular Users: (limited access)
Ticket Submission: Regular users can create new support tickets using a simple form. They need to provide a title, description of the issue, select a relevant department/category, and set a priority. Upon submission, the ticket will be recorded as "Open" and associated with the logged-in user. A success notification will inform the user that their ticket was created.
Viewing & Updating Tickets: Users have access to a personal dashboard listing their own tickets. They can view the details of each of their submitted tickets, including status updates from admins. Users can edit or update their tickets if, for example, they need to add information or if the issue is resolved on their side. (Note: Regular users cannot modify tickets submitted by others.)
Limited Visibility: Regular users can browse the list of departments (to understand categories of support) and see a list of other users in the system (e.g., to know the support staff or requestors). However, they cannot see the content of other users' tickets. They also cannot access any admin-only page; attempts to access admin URLs will be redirected with an error message.
Account Management: A regular user can update their own profile information (such as email, if that feature is provided in the UI) and change their password. They cannot elevate their privileges on their own. Any sensitive actions are restricted to admins.
Feedback: Just like admins, regular users receive flash message feedback. For example, if a form is submitted with missing information, they will see an error alert prompting them to correct it; if an update is successful, they get a confirmation message.
License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software as per the terms of the license. (For more details, see the LICENSE file in this repository, if provided.)
