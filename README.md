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
- Page styling is written in SCSS

## scss
If you wish to modify SCSS files and to compile them to CSS automatically when you modify the file you will have to go to sharwicom/mainapp/static/mainapp/scss and run:
You have to have [SCSS installed](https://sass-lang.com/install/)
```
sass --watch filename.scss ../css/filename.css
```
