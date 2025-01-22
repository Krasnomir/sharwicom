from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

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
            return HttpResponse("logged")
        
        template = loader.get_template('mainapp/login.html')
        context = {}

        return HttpResponse(template.render(context, request))

def register(request):
    if(request.method == "GET"):
        template = loader.get_template('mainapp/register.html')
        context = {}

        return HttpResponse(template.render(context, request))
    
    if(request.method == "POST"):
        firstName = request.POST["first-name"]
        lastName = request.POST["last-name"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(firstName, email, password)
        user.last_name = lastName

        user.save()

        template = loader.get_template('mainapp/register.html')
        context = {}

        return HttpResponse(template.render(context, request))

