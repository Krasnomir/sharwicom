import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.models import User
from .models import Conversation, Message, Content, Review
from django.contrib.auth import authenticate
from .validation import validate_register, validate_message, validate_content, validate_review
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, ContentForm, ReviewForm
from django.contrib.auth.decorators import login_required

def index(request):
    return redirect('home')

def home(request):
    template = loader.get_template('mainapp/home.html')
    context = {}

    user_conversations = get_non_empty_conversations(request.user)
    newest_contents = Content.objects.filter();

    template = loader.get_template('mainapp/home.html')
    context = {
        'convs':user_conversations,
        'contents':newest_contents
    }

    return HttpResponse(template.render(context, request))

# this function is responsible for removing empty conversations where a user (passed as a parameter) is participating
# returns a cleaned conversation array
def get_non_empty_conversations(user):
    # gets all conversations where the requesting user is participating including the empty ones
    conversations = Conversation.objects.filter(Q(person1=user) | Q(person2=user))
    non_empty_conversations = []

    for conversation in conversations:
        # tries to get at least one message object that is linked to the conversation
        message = Message.objects.filter(conversation=conversation).first()
        if message: # if no mesage was found
           non_empty_conversations.append(conversation)
    
    # return conversations, now without the empty ones
    return non_empty_conversations

@login_required
def conversations(request):
    user_conversations = get_non_empty_conversations(request.user)

    template = loader.get_template('mainapp/conversations.html')
    context = {'convs':user_conversations}

    return HttpResponse(template.render(context, request))

# loads a conversation page with a user specified by their username
@login_required
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
    user_conversations = get_non_empty_conversations(request.user)

    context = {
        'success': True,
        'messages': messages,
        'recipient_name': recipient_name,
        'convs': user_conversations
    }

    return HttpResponse(template.render(context, request))

def custom_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST) # create a form object and fill it with data from POST request
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # check if user has provided right username and password, if they did, log them in, if they didn't display the error message
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index') 
            else:
                form.add_error(None, "Incorrect username or password")
        else:
            form.add_error(None, "Captcha verification failed")
    else:
        form = LoginForm() # display an empty form if the request method is GET

    return render(request, 'mainapp/login.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST) # create a form object and fill it with data from POST request
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # additional checks like password strength
            validation_message = validate_register(username, first_name, last_name, email, password)
            
            if validation_message == 0: # if the validation was passed

                # create a new user object
                user = User.objects.create_user(first_name, email, password)
                user.last_name = last_name
                user.username = username
                user.save()
                
                login(request, user) # automatically login the user after they create an account

                return redirect('index') # redirect user to the homepage after successfull register
            else:
                form.add_error(None, validation_message) # display the validation error
        else:
            form.add_error(None, "Captcha verification failed")
    else:
        form = RegisterForm() # display an empty form if the request method is GET

    return render(request, 'mainapp/register.html', {'form': form})

# view for handling AJAX requests
def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('query')
        search_type = request.GET.get('type') # either "content" or "conversations" (for now)

        if(search_type == 'content'):
            search_results = Content.objects.filter(title__contains=search_query)

            # return users whose usernames match the query, in form of a JSON dictionary
            search_results_dict = [
                {"title": content.title, "type": content.type, "author": content.author, "url_name": content.url_name} for content in search_results
            ]

            return JsonResponse({'search_results': search_results_dict})
        
        elif(search_type == 'conversations'):
            search_results = User.objects.filter(username__contains=search_query)

            # return content that has a searched query in it's title
            search_results_dict = [
                {"username": user.username} for user in search_results
            ]

            return JsonResponse({'search_results': search_results_dict})


# view for handling AJAX requests
def sync_conversation(request):
    if request.method == 'GET':
        user_username = request.GET.get('user1', '')
        recipient_username = request.GET.get('user2', '')

        recipient = User.objects.get(username=recipient_username)

        if request.user.username == user_username:
            conversation = Conversation.objects.get((Q(person1=request.user) & Q(person2=recipient)) | (Q(person1=recipient) & Q(person2=request.user)))

            messages = Message.objects.filter(conversation=conversation).values('content', 'author__username', 'date')

            return JsonResponse({'success': 'true', 'messages': list(messages)})

# view for handling AJAX requests
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

# view for handling AJAX requests
def request_conversation(request):
    if request.method == 'GET':
        username = request.GET.get('username', '')
        recipient = User.objects.filter(username=username).first()
        if not recipient: # if a user with username specified in the request does not exist
            return JsonResponse({'success': 'false'})

        conversation = Conversation.objects.filter((Q(person1=request.user) & Q(person2=recipient)) | Q(person1=recipient) & Q(person2=request.user)).first() 

        if not conversation: # if there is no such existing conversation object create one
            newConversation = Conversation()
            newConversation.person1 = request.user
            newConversation.person2 = recipient
            newConversation.save()
            return JsonResponse({'success': 'true', 'createdConversation': 'true'})
        else:
            return JsonResponse({'success': 'true', 'createdConversation': 'false'})

# returns the average of all the ratings of a specified content
def get_community_rating(content):
    community_rating = 0

    for value in content.ratings.values():
        community_rating += int(value)

    if(community_rating != 0):
        return community_rating / len(content.ratings)
    
    return 0

def content(request, content_url_name):
    template = loader.get_template('mainapp/content.html')
    context = {}

    try: content = Content.objects.get(url_name=content_url_name)
    except: return HttpResponse(template.render({'success': False, 'message': "Content specified in the URL does not exist!"}, request))
    
    is_authenticated = True
    if not request.user.is_authenticated:
        is_authenticated = False

    user_rating = content.get_user_rating(request.user)
    community_rating = get_community_rating(content)
    
    # check if user has written a review for this content
    has_review = True
    try: Review.objects.get(Q(author=request.user) & Q(content=content)) 
    except: has_review = False

    context = {
        'success': True,
        'title': content.title,
        'url_name': content.url_name,
        'author': content.author,
        'type': content.type,
        'description': content.description,
        'user_rating': user_rating,
        'community_rating': community_rating,
        'reviews': Review.objects.filter(content=content),
        'has_review': has_review,
        'is_authenticated': is_authenticated
    }

    return HttpResponse(template.render(context, request))

# view for handling AJAX requests
def rate_content(request):
    if request.method == 'POST':

        if not request.user.is_authenticated:
            return JsonResponse({"success": False})
        
        data = json.loads(request.body)

        url_name = data.get('content_url_name')
        rating = data.get('rating')

        content = Content.objects.get(url_name=url_name)
        previous_rating = content.get_user_rating(request.user)

        if previous_rating != rating: # checks if the user picks a different rating from the previous time
            if int(rating) in {1,2,3,4,5}: # checks if rating is valid
                content.set_user_rating(request.user, rating)

                # update the user's review (if he has written one)
                review = Review.objects.filter(Q(author=request.user) & Q(content=content)).first()
                if review:
                    review.rating = rating
                    review.save()

                return JsonResponse({"success": True, "community_rating": get_community_rating(content)})
        
        return JsonResponse({"success": False})

    return HttpResponse('')

@login_required
def add_content(request):
    if request.method == 'POST': 
        form = ContentForm(request.POST) # create a form object and fill it with data from POST request

        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            type = form.cleaned_data['type']
            description = form.cleaned_data['description']
            url_name = title.lower() # convert all the characters from title to lowercase
            url_name = url_name.replace(" ",'-') # replace spaces with dashes

            validation_message = validate_content(url_name, author, type, description)

            if validation_message == 0: # if validation was successfull
                content = Content()

                content.title = title
                content.url_name = url_name
                content.author = author
                content.type = type
                content.description = description
                content.save()

                return redirect('content', url_name)
            else:
                form.add_error(None, validation_message) # display the validation error
        else:
            form.add_error(None, "Captcha verification failed")
    else:
        form = ContentForm() # display an empty form if the request method is GET

    return render(request, 'mainapp/add-content.html', {'form': form})

@login_required
def add_review(request, content_url_name):
    template = loader.get_template('mainapp/add-review.html')

    try: content = Content.objects.get(url_name=content_url_name)
    except Content.DoesNotExist: return HttpResponse(template.render({'success': False, 'message': "Content specified in the URL does not exist!"}, request))

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            summary = form.cleaned_data['summary']
            description = form.cleaned_data['description']

            validation_message = validate_review(content, summary, description, request.user, False)

            if validation_message == 0:
                review = Review()

                review.summary = summary
                review.description = description
                review.author = request.user
                review.content = content

                rating = content.get_user_rating(request.user) 
                if rating != None:
                    review.rating = rating

                review.save()
                return redirect('content', content.url_name)
            else:
                form.add_error(None, validation_message) # display the validation error
        else:
            form.add_error(None, "Captcha verification failed")
    else:
        form = ReviewForm() # display an empty form if the request method is GET

    context = {
        'success': True,
        'form': form,
        'url_name': content.url_name,
    }

    return render(request, 'mainapp/add-review.html', context)

@login_required
def edit_review(request, content_url_name):
    template = loader.get_template('mainapp/add-review.html')

    try: content = Content.objects.get(url_name=content_url_name)
    except Content.DoesNotExist: return HttpResponse(template.render({'success': False, 'message': "Content specified in the URL does not exist!"}, request))

    try: review = Review.objects.get(Q(author=request.user) & Q(content=content))
    except: return HttpResponse(template.render({'success': False, 'message': "This review does not exist!"}, request))

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            summary = form.cleaned_data['summary']
            description = form.cleaned_data['description']

            validation_message = validate_review(content, summary, description, request.user, True)

            if validation_message == 0:
                review = Review()

                review.summary = summary
                review.description = description
                review.author = request.user
                review.content = content

                rating = content.get_user_rating(request.user) 
                if rating != None:
                    review.rating = rating

                review.save()
                return redirect('content', content.url_name)
            else:
                form.add_error(None, validation_message) # display the validation error
        else:
            form.add_error(None, "Captcha verification failed")
    else:
        form = ReviewForm() # display an empty form if the request method is GET
        form = ReviewForm(initial={
            'summary': review.summary,
            'description': review.description,
        })

    context = {
        'success': True,
        'form': form,
        'url_name': content.url_name,
    }

    return render(request, 'mainapp/add-review.html', context)

def community(request, community_url_name):
    return HttpResponse('')
