# StudentHub 🎓

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![Status](https://img.shields.io/badge/Status-Active-22c55e?style=for-the-badge)](#)

A modern, institutional management web application designed for academic administrators, registrars, and educators. **StudentHub** centralizes student profiles, program assignments, roll-call attendance tracking, and financial fee collections into a high-performance dark-mode glassmorphic dashboard.

---

## 📖 About the Project

Managing student records, attendance sheets, and fee accounts across multiple spreadsheets can quickly become fragmented and error-prone. **StudentHub** provides a unified, frictionless solution for educational institutions.

### Core Objectives:
- **Streamlined Record Keeping:** Instant search, filtering, and enrollment tracking for students across academic programs.
- **Efficient Attendance Operations:** Single-click date-based attendance marking with rapid bulk toggles.
- **Financial Clarity:** Transparent student fee accounting with balance tracking and payment logs.
- **Modern Administrative Experience:** Designed with responsive, dark-mode glassmorphism and real-time visual analytics.

---

## ✨ Features

- 🔐 **Secure Authentication:** Session-based user authentication with hashed passwords (`scrypt`), protected routes, and role-based access.
- 📊 **Executive Dashboard:** Live metrics displaying total/active student counts, course breakdown charts, and recent enrollments.
- 👥 **Student Directory:** Searchable directory with course and status filters, profile details, and edit/delete controls.
- ➕ **Student Onboarding:** Register new students with automatic course assignment and fee account creation.
- 📋 **Classroom Attendance:** Daily roll calls with instant "Mark All Present/Absent" toggles and cumulative student attendance history.
- 💰 **Fee Management:** Track total fees, partial payments, outstanding balances, and last payment timestamps.
- 📥 **CSV Data Exports:** Export attendance reports and fee collection ledgers for external reporting.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, Flask, Werkzeug
- **Database:** MySQL 8.0+ via `mysql-connector-python`
- **Frontend:** Semantic HTML5, Custom CSS3 (Glassmorphism & Neon Dark Theme), Vanilla JavaScript
- **Visualization:** Chart.js

---

## 📁 Project Structure

```text
StudentsHUbB/
├── appp.py                # Main Flask application and API route controllers
├── database.py            # MySQL database connection helper
├── db_config.py           # Database credentials configuration
├── studenthub.sql         # Database schema & sample seed data
├── requirements.txt       # Python package dependencies
├── README.md              # Project documentation and setup guide
├── static/
│   ├── hero_students.jpg  # Hero banner illustration
│   ├── script.js          # Client-side UI interactions and chart logic
│   └── style.css          # Theme styles and glassmorphic UI components
└── templates/
    ├── base.html          # Base layout with navigation and footer
    ├── index.html         # Executive dashboard & analytics
    ├── login.html         # Sign-in portal
    ├── students.html      # Student directory & management
    ├── add_students.html  # Student registration form
    ├── attendance.html    # Daily roll-call attendance sheet
    ├── fees.html          # Fee collection and balance tracking
    └── about.html         # System architecture and information
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+** installed
- **MySQL Server 8.0+** running locally or remotely
- **Git**

### 2. Clone the Repository
```bash
git clone https://github.com/Rishmith50/StudentsHUbB.git
cd StudentsHUbB
```

### 3. Create and Activate Virtual Environment
```powershell
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup the MySQL Database
Import the provided [studenthub.sql](studenthub.sql) script into your MySQL server:
```bash
mysql -u root -p < studenthub.sql
```
*(Or import `studenthub.sql` using MySQL Workbench / phpMyAdmin).*

### 6. Configure Database Credentials
Edit `db_config.py` with your MySQL connection details:
```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "studenthub"
}
```

### 7. Run the Application
```bash
python appp.py
```
Open your browser and navigate to **`http://127.0.0.1:5000`**.

---

## 🔑 Default Credentials

For initial testing, you can log in with the seeded administrator account:

- **Username:** `admin`
- **Password:** `admin123`

---

## 👤 Author

Developed by **Rishmith** ([@Rishmith50](https://github.com/Rishmith50))
