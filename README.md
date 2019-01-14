# Tangerine

<p>Tangerine is a chatbot written in python using the Django web framework.</p>

![alt text](https://github.com/raabyau/tangerine/blob/master/screenshot.png)


## Dependencies

Python 3.6<br/>
Django 2.1.5<br/>
Django channels 2.1.6<br/>
PostgreSQL 10.5

## Installation / Setup

<p>
- Clone the repository:
  ```
  git clone https://github.com/raabyau/tangerine.git"
  ```
  
- Create a PostgreSQL database for the application and then update settings.py with the database name, username and password.<br/>
- Install Django. "pip install django"<br/>
- Install Django Channels. "pip install channels"</br>
- Install Postgres python adapter. "pip install psycopg2"<br/>
- Perform Django migrations from the root project directory. "python manage.py makemigrations" and "python manage.py migrate".</br>
- Create a superuser that can be used to login to the admin site. "python manage.py createsuperuser".</br>
- Run the development server. "python manage.py runserver".</br>
- Open the admin site, http://127.0.0.1:8000/admin/ and populate the Question and Questionnaire tables with the JSON found <a href="https://github.com/raabyau/tangerine/tree/master/demo">here</a>. Make sure the <b>name</b> attributes are populated with "demo_questions" and "demo_questionnaire" respectively.</br>
- Open http://127.0.0.1 and chat away!!

</p>
