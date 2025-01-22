from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('mainapp/main.html')
    context = {}

    return HttpResponse(template.render(context, request))

def login(request):
    template = loader.get_template('mainapp/login.html');
    context = {}

    return HttpResponse(template.render(context, request))

def register(request):
    template = loader.get_template('mainapp/register.html');
    context = {}

    return HttpResponse(template.render(context, request))
