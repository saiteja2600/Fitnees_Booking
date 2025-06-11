🏋️‍♂️ Fitness Studio Booking System

A web-based application for managing a fitness studio, built using Django. It provides two separate panels:
    • Admin Panel: To manage trainers, classes, and class schedules.
    • User Panel: To register, log in, view class schedules, and book fitness sessions.
This project was developed as part of the Python Developer Assignment 2025 to demonstrate backend development, API design, and system structuring using Django.

🚀 Features
	👨‍💼 Admin Panel
    • Admin authentication
    • Add/edit/delete Trainers
    • Add/edit/delete Class schedules
    • View available classes in a calendar view
    • Logout functionality
	🧑‍💻 User Panel
    • User registration & login
    • View available classes
    • Book a class by selecting date, trainer, and time
    • View personal class schedule in a calendar
	⚙️ Tech Stack
 	| Area          | Stack/Tool Used            |
| ------------- | -------------------------- |
| Backend       | Python, Django             |
| Frontend      | HTML, CSS, Bootstrap       |
| Database      | SQLite (Default Django DB) |
| Calendars     | FullCalendar.js            |
| UI Components | Font Awesome, SweetAlert2  |
| Tooltips      | Tippy.js                   |

 🛠 Setup Instructions
 		Prerequisites
    • Python 3.8+
    • virtualenv (recommended)
	# Clone the repo
git clone https://github.com/<your-username>/fitness-studio-booking.git
cd fitness-studio-booking

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Run the server
python manage.py runserver


📩 Sample Requests

🔎 View Available Classes

GET /available_classes/
POST /book/
{
  "class_id": 3,
  "client_name": "John Doe",
  "client_email": "john@example.com"
}

📋 Get Bookings by Email
GET /bookings?email=john@example.com

📦 Seed Data
You can manually add sample classes and trainers through the Django Admin Panel or the Admin Dashboard after login.

✅ Evaluation Highlights
✔️ Modular Views and Template Inheritance

✔️ FullCalendar Integration for UX

✔️ SweetAlert for cleaner user interaction

✔️ Admin/User segregation

✔️ Fully tested on local server

