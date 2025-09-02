# Vacation Management System

This project is part of the Python Full Stack Web Developer course – Part II. It’s a web application built with Django that allows users to register, log in, and interact with a list of vacation packages. Admin users can also manage (add, edit, delete) vacation entries.

GitHub Link: https://github.com/GeorgeMagnuss/secondproject

## Student Info

- **Name**: George Mattar

---

## What the App Does

### For All Users:
- Register or log in using email and password
- View a list of available vacation packages (with 3 cards per row)
- Like or unlike any vacation
- Log out

### For Admins:
- Access a separate admin-only page
- Add new vacations
- Edit existing ones
- Delete vacations (with confirmation)
- View how many likes each vacation has

---

## Tech Stack

- **Backend**: Python 3.12, Django 5.2.4
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (with PostgreSQL-ready support)
- **Other tools**: Pillow (for image uploads)

---

## Database Models

The app uses the following tables:

### Roles
- `id`
- `role_name` (Admin / User)

### Users (custom user model)
- `id`, `first_name`, `last_name`, `email`, `password`, `role`

### Countries
- `id`, `country_name`

### Vacations
- `id`, `country`, `description`, `start_date`, `end_date`, `price`, `image_file`

### Likes
- `user`, `vacation` (composite primary key)

---

## Setup Instructions

### Requirements:
- Python 3.8+
- Virtual environment (venv)

### 1. Clone the project
```bash
cd /path/to/VacationProjectGM
