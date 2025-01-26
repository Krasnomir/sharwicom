from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from .models import Conversation, Message
from django.contrib.auth import authenticate
from .validation import validate_register, validate_message
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

def index(request):
    return redirect('home')

def home(request):
    template = loader.get_template('mainapp/home-base.html')
    context = {}

    return HttpResponse(template.render(context, request))

def conversations(request):
    # gets all conversations where the requesting user is participating
    user_conversations = Conversation.objects.filter(Q(person1=request.user) | Q(person2=request.user))

    template = loader.get_template('mainapp/conversations.html')
    context = {'convs':user_conversations}

    return HttpResponse(template.render(context, request))

# loads a conversation page with a user specified by their username
def conversation(request, recipient_name):

    # user sends a message
    if request.method == "POST":
        message_content = request.POST["message-content"]
        
        validation_message = validate_message(message_content)

        # if validation was successfull, currently if it isn't it doesn't display the error anywhere
        if validation_message == 0:
            recipient = User.objects.get(username=recipient_name)
            conversation_object = Conversation.objects.get((Q(person1=request.user) & Q(person2=recipient)) | (Q(person1=recipient) & Q(person2=request.user)))

            new_message = Message.objects.create(content=message_content,author=request.user,conversation=conversation_object)
            new_message.save()
        

    template = loader.get_template('mainapp/conversation.html')

    # the user with which we're conversating 
    # returns an error message if it didn't find anything
    try: user = User.objects.get(username=recipient_name)
    except: return HttpResponse(template.render({'success': False, 'message': "A user specified in the URL does not exist!"}, request))
    
    # get the conversation with the requesting user and the user specified in the url
    # returns an error message if it didn't find anything
    try: conversation = Conversation.objects.get((Q(person1=request.user) & Q(person2=user)) | (Q(person1=user) & Q(person2=request.user)))
    except: return HttpResponse(template.render({'success': False, 'message': "Didn't find a conversation with that user!"}, request))

    messages = Message.objects.filter(conversation=conversation)

    # gets all conversations where the requesting user is participating
    # this is just to display all the active conversations in the left pane
    user_conversations = Conversation.objects.filter(Q(person1=request.user) | Q(person2=request.user))

    context = {
        'success': True,
        'messages': messages,
        'recipient_name': recipient_name,
        'convs': user_conversations
    }

    return HttpResponse(template.render(context, request))

def custom_login(request):
    template = loader.get_template('mainapp/login.html')
    context = {}

    # redirects to the index page if the username and the password are correct and displays a message if they aren't
    if(request.method == "POST"):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)

        if user is not None:
            if request.user.is_authenticated:
                logout(request)
            
            login(request, user)
            return redirect('index')
        else:
            context = {'error_message': "Incorrect username or password"}

    return HttpResponse(template.render(context, request))

def register(request):
    template = loader.get_template('mainapp/register.html')
    context = {}

    if(request.method == "POST"):
        username = request.POST["username"]
        first_name = request.POST["first-name"]
        last_name = request.POST["last-name"]
        email = request.POST["email"]
        password = request.POST["password"]

        # display what is wrong with the inputted data or add the new account to the database and redirect user to the index page
        validationMessage = validate_register(username, first_name, last_name, email, password)
        if(validationMessage) == 0:
            user = User.objects.create_user(first_name, email, password)
            user.last_name = last_name
            user.username = username

            user.save()

            return redirect('index')
        else:
            # this is just to save the inputted data so the user won't have to fill all the fields again
            context = {
                'error_message': validationMessage,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password,
            }

    return HttpResponse(template.render(context, request))

