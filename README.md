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
- [Automative-testing](#automative-testing)
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

<table style="width:100%">
  <tr>
    <th>Testing environment</th>
    <th>Testing tool</th>
    <th>Expected outcome</th>
    <th>Errors reported</th>
    <th>Further actions</th>
  </tr>

  <tr>
  <td>Home Page</td>
  <td>The official W3C validator website</td>
  <td>The page to function as intended, to display and render two internal links;the register and login links.</td>
  <td>Two different elements were named with an identical Ids.</td>
  <td>The reported bug was fixed by renaming the Id of one of the elements.</td>
  </tr>

   <tr>
  <td>Register Page</td>
  <td>The official W3C validator website</td>
  <td>The page to function as intended, to display and render a form asking users to provide name, email and password. There is also a register button and a link to go back to the home page.</td>
  <td>No defects presented</td>
  <td>No further action required.</td>
  </tr>

  <tr>
  <td>Login Page</td>
  <td>The official W3C validator website</td>
  <td>The page to function as intended, to display and render a form asking users to provide email and password. There is also a login button and a link to go back to the home page.</td>
  <td>No defects presented</td>
  <td>No further action required.</td>
  </tr>

  <tr>
  <td>User Dashboard</td>
  <td>The official W3C validator website</td>
  <td>The page to function as intended, to display existing bookings or/and enable users to create a new booking. There is also a logout button and a link to go back to the login page. The page also inludes edit and delete buttons to aid the user manipulate data.</td>
  <td>This was first created with sqlite3, a relational database system that embeds into applications directly. This has caused an error and prevented the app from being deployed on Heroku.</td>
  <td>The entire relational database system was changed into psycopg2, which is PostgreSQL database for python programing language. This enabled me to successfully deploy the app on Heroku.</td>
  </tr>

  <tr>
  <td>Admin Dashboard</td>
  <td>The official W3C validator website</td>
  <td>The page to function as intended, to display existing bookings of all registered users of the app. There is also a logout button and a link to go back to the login page. The page also inludes status and action columns to aid the admin manipulate data.</td>
  <td>This was first created with sqlite3, a relational database system that embeds into applications directly. This has caused an error and prevented the app from being deployed on Heroku.</td>
  <td>The entire relational database system was changed into psycopg2, which is PostgreSQL database for python programing language. This enabled me to successfully deploy the app on Heroku.</td>
  </tr>

   <tr>
  <td>CSS custom page</td>
  <td>W3 Jigsaw CSS validor</td>
  <td>Apply desired styles and layouts to selected elements, as well as enhanced readability and semantics.</td>
  <td>No defects presented.</td>
  <td>No further action required.</td>
  </tr>

  <tr>
  <td>Internal links</td>
  <td>All buttons and linked explored and double checked in all pages.</td>
  <td>Users not to encounter broken links when intending to prompt desired actions in the website.</td>
  <td>No bugs detected whatsoever.</td>
  <td>No action required.</td>
  </tr>

  <tr>
  <td>Responsiveness</td>
  <td>Using the latest version of bootstrap and media queries on the CSS custom page to ensure a consistent user experience whether accessed on a desktop computer, tablet or mobile phones</td>
  <td>So that users have the ability to adjust and adapt automatically to all media screen sizes.</td>
  <td>No errors.</td>
  <td>Not needed.</td>
  </tr>

  <tr>
  <td>JavaScript file</td>
  <td>The offical JSLint code analysis tool</td>
  <td>To statically and automatically analyse if the JavaScript source code we provided for our project complies with coding rules.</td>
  <td>Two different functions were named with an identical name, and the second function was over-writing the first.</td>
  <td>The name for the second function was changed and no further action was required.</td>
  </tr>
  </table>

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


## Automative-testing

Automative testing framework that is designed to make sure correctness of any codebase written by developers. This particular framework will allow you to write tests with an approachable, well known and highly interactive API that gives you results quickly.<br>

Manual website testing is conducted by human testers manually checking the website through interaction with the site developed. Testers usually follow test cases but they can also explore freely. Manual testing is best for usability testing, exploratory testing and UI validation. On the other hand automative website testing uses scripts and software tools like Selenium or Cypress. This type of testing can run tests on multiple browsers and devices automatically. Automative website testing is best for regression testing, load testing and repetitive tasks.<br>

Since 99% of the language used in this project was Python, it is only rational to include a Python testing methods to detect if any errors are presents in the functions and semantics of the files in my project.

- All forms in the register and login pages have passed the automative tests with no erros detected. 
<div class="column">
    <img src="static/tests/images/automated_test_forms.jpg" alt="automative tests for all forms validated" style="width:50%">
  </div>

- The new booking page for users to submit their holiday period after they have loged in was validated with aumative tests.
<div class="column">
    <img src="static/tests/images/automated_test_new_booking.jpg" alt="automative tests for the new booking page validated" style="width:50%">
  </div>

- The admin page to view and approve the holiday period requested by users was validated in automative testing method with no bugs found. 
<div class="column">
    <img src="static/tests/images/automated_test_admin.jpg" alt="automative tests for the admin page validated" style="width:50%">
  </div>


  
