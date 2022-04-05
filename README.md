This is a chat application, implemented using Flask-SocketIO with both the database (PostgreSQL)
Files in the program
application.py: This is the main app file and contains both the registration/login page logic and the Flask-SocketIO backend for the app.
models.py: Contains Flask-SQLAlchemy models used for user registration and login in application.py
wtform_fields.py: Contains the classes for WTForms/Flask-WTF and the custom validators for the fields
requirements.txt: list of Python packages installed
templates/: folder with all HTML files
static/: for with all JS scripts and CSS files
My personal touch is the wtf forms module which i used for my login and registration