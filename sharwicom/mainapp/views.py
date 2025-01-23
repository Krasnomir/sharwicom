from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .validation import validateRegister

# TODO: Register data validation

def index(request):
    template = loader.get_template('mainapp/main.html')
    context = {}

    return HttpResponse(template.render(context, request))

def login(request):
    if(request.method == "GET"):
        template = loader.get_template('mainapp/login.html')
        context = {}

        return HttpResponse(template.render(context, request))
    if(request.method == "POST"):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)

        if user is not None:
            return redirect('index')
        else:
            template = loader.get_template('mainapp/login.html')
            context = {'error_message': "Incorrect username or password"}

            return HttpResponse(template.render(context, request))

def register(request):
    if(request.method == "GET"):
        template = loader.get_template('mainapp/register.html')
        context = {}

        return HttpResponse(template.render(context, request))
    
    if(request.method == "POST"):
        username = request.POST["username"]
        firstName = request.POST["first-name"]
        lastName = request.POST["last-name"]
        email = request.POST["email"]
        password = request.POST["password"]

        validationMessage = validateRegister(username, firstName, lastName, email, password)
        if(validationMessage) == 0:
            user = User.objects.create_user(firstName, email, password)
            user.last_name = lastName
            user.username = username

            user.save()

            template = loader.get_template('mainapp/register.html')
            context = {}

            return HttpResponse(template.render(context, request))
        else:
            template = loader.get_template('mainapp/register.html')
            context = {
                'error_message': validationMessage,
                'username': username,
                'first_name': firstName,
                'last_name': lastName,
                'email': email,
                'password': password,
            }

            return HttpResponse(template.render(context, request))

