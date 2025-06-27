# Help Desk Ticketing System

A simple, secure Python web application to manage support tickets within an organisation. Built for Level 5 Software Engineering & Agile coursework, it demonstrates modular coding, secure user management, and Agile best practices.

---

## Features

- **Role-based Access:**  
  - Admin: Full Create, Read, Update, Delete (CRUD) on all tickets and users  
  - User: Can Create, Read, Update their own tickets  
- **User Authentication:** Registration and login required  
- **Input Validation:** Prevents invalid entries with clear error messages  
- **Usability:** Flash notifications for actions, confirmation prompts for deletes  
- **Modular & Secure:** Uses Python (Flask), SQLite, password hashing, and clear code structure  
- **Seeded Demo Data:** Initial admin and user accounts, sample tickets/departments  

---

## Technology Stack

- Python 3, Flask, Flask-SQLAlchemy, Flask-Login, WTForms, Bootstrap 5  
- SQLite database (file-based, zero-config)  
- See `requirements.txt` for all dependencies

---

## Quick Start

1. **Clone this repo:**
  git clone https://github.com/yourusername/yourrepo.git
  cd yourrepo

3. **Create a virtual environment & install dependencies:**
   python -m venv venv
   source venv/bin/activate # Windows: venv\Scripts\activate
   pip install -r requirements.txt

3. **Seed the database with demo data:**
   python seed.py

4. **Run the application:**
   python app.py

5. **Open in your browser:**  
Go to [http://localhost:5000](http://localhost:5000)

---

## Demo Login Credentials

Use these accounts to log in immediately:

| Role  | Email               | Password    |
|-------|---------------------|-------------|
| Admin | admin@example.com   | Admin@123   |
| User  | user@example.com    | User@123    |

You can also register a new account on the registration page.

---

## Basic Usage

- **Admins can:**  
- Manage all tickets, users, and departments  
- Delete records with confirmation  
- Receive feedback via notifications  
- **Users can:**  
- Submit new tickets  
- View and update their own tickets  
- Update their profile

---

## Best Practices

- Modular code (Blueprints or separate modules for admin, user, models, etc.)
- All sensitive data (passwords) hashed securely
- Clear, consistent naming and comments
- Form validation, error handling, and user feedback on every action
- Secure default configuration (use environment variables for production)

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---





