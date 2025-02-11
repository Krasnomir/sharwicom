import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.models import User
from .models import Conversation, Message, Content
from django.contrib.auth import authenticate
from .validation import validate_register, validate_message, validate_content
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

def sync_conversation(request):
    if request.method == 'GET':
        user_username = request.GET.get('user1', '')
        recipient_username = request.GET.get('user2', '')

        recipient = User.objects.get(username=recipient_username)

        if request.user.username == user_username:
            conversation = Conversation.objects.get((Q(person1=request.user) & Q(person2=recipient)) | (Q(person1=recipient) & Q(person2=request.user)))

            messages = Message.objects.filter(conversation=conversation).values('content', 'author__username', 'date')

            return JsonResponse({'success': 'true', 'messages': list(messages)})

def send_conversation(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        sender_username = data.get('sender')
        recipient_username = data.get('recipient')
        message_content = data.get('message_content')

        if sender_username == request.user.username:
            validation_message = validate_message(message_content)

            # if validation was successfull, currently if it isn't it doesn't display the error anywhere
            if validation_message == 0:
                recipient = User.objects.get(username=recipient_username)
                conversation_object = Conversation.objects.get((Q(person1=request.user) & Q(person2=recipient)) | (Q(person1=recipient) & Q(person2=request.user)))

                new_message = Message.objects.create(content=message_content,author=request.user,conversation=conversation_object)
                new_message.save()

            return HttpResponse("")

        return HttpResponse("")

def content(request, content_url_name):
    template = loader.get_template('mainapp/content.html')

    try: content = Content.objects.get(url_name=content_url_name)
    except: return HttpResponse(template.render({'success': False, 'message': "Content specified in the URL does not exist!"}, request))
    
    user_rating = content.get_user_rating(request.user)
    community_rating = 0
    
    for value in content.ratings.values():
        community_rating += int(value)

    community_rating = community_rating / len(content.ratings)
    
    context = {
        'success': True,
        'title': content.title,
        'url_name': content.url_name,
        'author': content.author,
        'type': content.type,
        'description': content.description,
        'user_rating': user_rating,
        'community_rating': community_rating,
    }

    return HttpResponse(template.render(context, request))

def add_content(request):
    context = {}

    if request.method == 'POST':
        
        title = request.POST['title']
        author = request.POST['author']
        type = request.POST['type']
        description = request.POST['description']
        url_name = title.lower() # convert all the characters from title to lowercase
        url_name = url_name.replace(" ",'-') # replace spaces with dashes

        validation_message = validate_content(url_name, author, type, description)

        if validation_message == 0:
            content = Content()

            content.title = title
            content.url_name = url_name
            content.author = author
            content.type = type
            content.description = description
            content.save()
        else:
            context = {
                'error_message': validation_message,
                'title': title,
                'author': author,
                'description': description
            }

    template = loader.get_template('mainapp/add-content.html')
    return HttpResponse(template.render(context, request))

def rate_content(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        url_name = data.get('content_url_name')
        rating = data.get('rating')

        content = Content.objects.get(url_name=url_name)
        previous_rating = content.get_user_rating(request.user)

        if previous_rating != rating: # checks if the user picks a different rating from the previous time
            if int(rating) in {1,2,3,4,5}: # checks if rating is valid
                content.set_user_rating(request.user, rating)
                return JsonResponse({"success": True})
                
        return JsonResponse({"success": False})

    return HttpResponse('')
