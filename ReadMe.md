# Social Media with Django

 
The app provide a features as social media does : Registration , Posting , Follow , Interacting with posts .
The app created using **Django**  and sqlLite.
This is a basic application with Django, but it uses fundamental techniques.
## How to run

1. To create a database from our models.
```bach 
cd /path/app/
python3 manage.py makemigrations
``` 

2. Apply these migrations to our database.
```bach 
python3 manage.py migrate
``` 
## Start the server

To Start the server run :

```bach 
python3 manage.py runserver
``` 
## Tree

```bach 

..
├── db.sqlite3
├── LICENSE
├── manage.py
├── network
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── static
│   │   └── network
│   │       ├── jquery.js
│   │       ├── main.js
│   │       └── styles.css
│   ├── templates
│   │   └── network
│   │       ├── following.html
│   │       ├── index.html
│   │       ├── layout.html
│   │       ├── login.html
│   │       ├── register.html
│   │       └── user.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── project4
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── ReadMe.md

10 directories, 56 files
```
	
## Contact

This is a basic app with django however ,it use the fondamental techniques . Please don't hesitate to contact me .
