# Tangerine

Tangerine is a chatbot web application written in python using the Django web framework.

## Dependencies

Python 3.6<br/>
Django 2.1.5. https://www.djangoproject.com<br/>
PostgreSQL 10.5

## Installation / Setup

<p>
1. Clone the repository. "git clone https://github.com/raabyau/tangerine.git"</br>
2. Create a PostgreSQL database for the application and then update settings.py with the database name, username and password.<br/>
3. Install Django. "pip install django"<br/>
4. Install Django Channels. "pip install channels"</br>
5. Perform Django migrations from the root project directory. "python manage.py makemigrations" and "python manage.py migrate".</br>
6. Create a superuser that can be used to login to the admin site. "python manage.py createsuperuser".</br>
7. Run the development server. "python manage.py runserver".</br>
8. Open the admin site, http://127.0.0.1:8000/admin/ and populate the Question and Questionnaire tables with the JSON found here. Make sure the <b>name</b> attributes are populated with "demo_questions" and "demo_questionnaire" respectively.</br>
9. Open http://127.0.0.1 and chat away!!

</p>
