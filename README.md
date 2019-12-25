# Project 1

Web Programming with Python and JavaScript

Dependencies & Tech stack:
- Requirements.txt document
- Python
- Flask
- PostgreSQL(Heroku DB)
- JQuery
- AJAX

How to Run:
pip install -r requirements.txt to gather proper req's

After cloning from git:
1. Navigate to the top level of the app that includes the Flaskr folder, books.csv, requirements.txt and others
2. From here set the Env variable to be the Flaskr folder - I use a MAC so I used export FLASK_APP=flaskr
3. Execute flask run command and the app should start

Requirements - For more details on each file, please see comments inside them

Registration/Login/Logout: users are able to register, login and logout via the nav buttons. This is controlled by the auth.py blueprint and /auth html files. User is tracked in session until they log out or session expires. Users stored in DB table users

Import: import.py checks if a table exists and imports to a books table using the current DB configuration.

Search: User must be logged in to search. AJAX real time search that searches wild card on ISBN, Author and Book name. Clicking on the view link for a result will take you to the book's page. Search is initiated after 3 characters or more to accommodate performance

Book Page: The main index shows the first 10 results of books, mainly for flavor. Once a user is logged in, the "View" link is presented and allows users to see specific book pages. Here the user sees an overview of the book. If retrieved correctly, the user is also shown the GoodReads.com API results for book reviews. If there are any site-specific reviews, those are also displayed. The user is also able to submit their own reviews. A user cannot submit a review twice.
    ^^Individual book page link structure/route: rootdir/api/id where id is the internal id of the book in the DB. Example: http://localhost:5000/api/3729

Review Submission: The user is also able to submit their own reviews from any individual book's page. A user cannot submit a review twice.

Goodreads Review Data: The user is able to see the GoodReads data for that book from any individual book's page.

API Access: User can reach the JSON API by accessing: rootdir/api/ISBN/json where ISBN is the exact ISBN of the book they are searching for. A non-found result will show a 404 page. Example: http://localhost:5000/api/0380795272/json

App Structure and Methods
(more detail in the comments of each file and method)

Main App:
__init__.py - Initiates app and sets blueprints
auth.py - Handles register, login and logout and session logic, including a decorator that ensures users are logged in to user certain pages and methods
blog.py - Handles the majority of books logic, including rendering index, search, books pages, JSON API and others

Database:
database.ini - DB config file with DB credentials. Intentionally included as this is a test DB instance
db.py - handles DB connection in a centralized location. This is called from various app pages and returns a db connection object
dbconfig.py - parses and handles the DB config file

Static:
/templates/auth - Various templates for login pages
/templates/blog - Various templates for books pages
base.html - base HTML page that is extended by all pages above
404.html - 404 page
/scripts/ajaxsearch.js - JS logic for AJAX book search
style.css - CSS file

Misc:
books.csv - initial csv file of 50,000 books
import.py - imports the above CSV file into a books table (creates it if it doesn't exist)
