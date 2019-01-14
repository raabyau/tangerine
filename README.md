# Tangerine

Tangerine is a chatbot written in python using the Django web framework.

![alt text](https://github.com/raabyau/tangerine/blob/master/screenshot.png)


## Dependencies

* Python 3.6
* Django 2.1.5
* Django channels 2.1.6
* PostgreSQL 10.5 (or a version that support JSON fields)

## Installation / Setup

Clone the repository:
```
git clone https://github.com/raabyau/tangerine.git
```

Install Django, Django channels and the Postgres python adapter:
```
pip install django
pip install channels
pip install psycopg2
```

Create a PostgreSQL database for the application and then update settings.py with the database name, username and password.

Perform Django migrations from the root project directory:
```
python manage.py makemigrations
python manage.py migrate
```

Create a superuser that can be used to login to the admin site:
```
python manage.py createsuperuser
```

Run the development server
```
python manage.py runserver
```

Open the admin site, http://127.0.0.1:8000/admin/ and populate the Question and Questionnaire tables with the JSON found <a href="https://github.com/raabyau/tangerine/tree/master/demo">here</a>. Make sure the <b>name</b> attributes are populated with "demo_questions" and "demo_questionnaire" respectively.

Open http://127.0.0.1 and chat away!!
