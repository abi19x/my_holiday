# My Holiday - Holiday Booking Application

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

My Holiday is a full-stack web application that allows users to book holidays while administrators manage bookings and user access. It is built with Flask, PostgreSQL, and is deployed on Heroku.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Images](#images)
- [Installation](#installation)
- [Usage](#usage)
- [Admin Access](#admin-access)
- [Technologies Used](#technologies-used)
- [Deployment](#deployment)
- [Credits](#credits)
- [Testing](#testing)
- [License](#license)

## Overview

This app allows users to:
- Register and log in securely
- Submit and view holiday booking requests
- Receive booking status updates

Admin users can:
- View all bookings
- Change booking statuses
- Manage users

## Features

- User registration and login system
- Admin dashboard with role-based access control
- Database integration with PostgreSQL
- Mobile responsive design using Bootstrap
- Deployment-ready with Heroku support

## Images

<div class="row">
  <div class="column">
    <img src="static/images/home_page.jpg" alt="App's homepage" style="width:70%">
  </div>
  <div class="column">
    <img src="static/images/register_page.jpg" alt="App's register page" style="width:70%">
  </div>
  </div>

  <div class="row">
  <div class="column">
    <img src="static/images/login_page.jpg" alt="App's login page" style="width:70%">
  </div>
  <div class="column">
    <img src="static/images/dashboard_page.jpg" alt="App's dashboard page" style="width:70%">
  </div>
  </div>

  <div class="row">
  <div class="column">
    <img src="static/images/new_booking_page.jpg" alt="App's new booking page" style="width:70%">
  </div>
  <div class="column">
    <img src="static/images/admin_page.jpg" alt="App's admin page" style="width:70%">
  </div>
  </div>

## Installation

1. Clone the repository:
``bash
- git clone https://github.com/abi19x/my_holiday
- cd my_holiday

2. **Set up a virtual environment**:
- python3 -m venv venv
- source venv/bin/activate

3. **Install dependencies**:
- pip install -r requirements.txt

4. **Set environment variables**:
- export FLASK_APP=run.py
- export FLASK_ENV=development
- export DATABASE_URL=your-database-url

5. **Initialize the database**:

- from models.db import init_db
- from app import app
- init_db(app)

6. **Run the app locally**:
- python3 run.py runserver

## Usage

- Users can register, login, and book holidays
- Admins can log in and access the **/admin** dashboard to **view and manage bookings**

## Admin Access

To manually create an admin user on Heroku:
1. **Retrieve the database URL:**
heroku config:get DATABASE_URL -a my-holiday
2. **Run an interactive shell on Heroku:**
heroku run python -a my-holiday
3. **Create the admin user:**
import psycopg
from werkzeug.security import generate_password_hash

db_url = "PASTE_YOUR_HEROKU_DATABASE_URL_HERE"
conn = psycopg.connect(db_url)
cur = conn.cursor()

hashed_pw = generate_password_hash("your-password")

cur.execute("""
    INSERT INTO users (name, email, password, role)
    VALUES (%s, %s, %s, %s);
""", ("admin", "admin@example.com", hashed_pw, "admin"))

conn.commit()
cur.close()
conn.close()

## Technologies Used

- **Flask** - Lightweight Python web framework
- **PostgreSQL** - Relational database management
- **psycopg** - PostgreSQL database adapter
- **Werkzeug** - Secure password hashing
- **Bootstrap** - Frontend UI framework
- **Heroku** - Cloud application platform

## Deployment (Heroku)

**To deploy the app on Heroku:**
- heroku create my-holiday
- heroku addons:create heroku-postgresql:hobby-dev
- git push heroku main
- heroku run python

## Credits

- **Code Institute** - Project structure and inspiration
- **Flask and Psycopg Documentation**
- **Bootstrap** - For frontend styling and responsive design
- **Werkzeug** - For generating and checking password hash 
- **Heroku** For documentation and providing a cloud application platform for project deployment

## Testing

- The homepage was validated through the official W3C validator website and there were no bugs detected. See the image below.<br>
 <div class="column">
    <img src="static/tests/images/homepage_validated.jpg" alt="Homepage validated" style="width:50%">
  </div>

- The register and login pages were validated through the official W3C validator website and there were no errors detected. See the respected images below.<br>
<div class="column">
    <img src="static/tests/images/register_page_validated.jpg" alt="Register page validated" style="width:50%">
  </div>
  <div class="column">
    <img src="static/tests/images/login_page_validated.jpg" alt="Login page validated" style="width:50%">
  </div>

- The dashboard and admin pages were validated through the official W3C validator website and there were no bugs found in both pages. See the respected images below.<br>
 <div class="column">
    <img src="static/tests/images/dashboard_validated.jpg" alt="Dashboard page validated" style="width:50%">
  </div>
  <div class="column">
    <img src="static/tests/images/admin_page_validated.jpg" alt="Admin page validated" style="width:50%">
  </div>

- The new booking page was validated through the official W3C validator website and there were no bugs detected. See the image below.<br>
  <div class="column">
    <img src="static/tests/images/new_booking_page_validated.jpg" alt="New booking page validated" style="width:50%">
  </div>

- I have confirmed multiple times that the main page is linked rightfully to the custom CSS file. I can now confirm that the custom CSS file in this project passes through the official W3 Jigsaw CSS validor with no issues. See the screenshot below. 
<div class="column">
    <img src="static/tests/images/css_validated.jpg" alt="Custom CSS file validated" style="width:50%">
  </div>

  
