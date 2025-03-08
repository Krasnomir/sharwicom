# sharwicom
Django web application for content reviewing and rating.

## dependencies
You need to have python installed.
The project uses following python modules:
- Django
- Django-simple-captcha

## installation
Go to /sharwicom/ directory in project root folder

Windows:
```
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```

Unix based:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

The app will run on the port 8000, type in localhost:8000 in your browser search bar to access it

## features
- User sessions
- Captcha verification
- Conversations
- AJAX requests
- Search bars
- Content reviews and ratings
