import re
from django.contrib.auth.models import User
from .models import Content, content_types, Review
from django.db.models import Q

# goes over and checks all the fields in the same order as they are passed as parameters
# returns the error message or 0 if the data is correct
def validate_register(username, first_name, last_name, email, password):

    # check if username is already taken
    if User.objects.filter(username=username).exists():
        return "Username is already taken"

    # validate username: 3-20 characters, only letters and numbers
    userrname_pattern = r'^[a-zA-Z0-9]{3,20}$'
    if not re.match(userrname_pattern, username):
        return "Username must be 3-20 characters long and contain only letters and numbers."
    
    # validate first name: 2-50 characters, letters only
    first_name_pattern = r'^[a-zA-Z]{2,50}$'
    if not re.match(first_name_pattern, first_name):
        return "First name must be 2-50 characters long and contain only letters."
    
    # validate last name: 2-50 characters, letters only
    last_name_pattern = r'^[a-zA-Z]{2,50}$'
    if not re.match(last_name_pattern, last_name):
        return "Last name must be 2-50 characters long and contain only letters."

    # validate email: proper format
    email_pattern = r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)])'
    if not re.match(email_pattern, email, re.IGNORECASE):
        return "Invalid email format."
    
    # validate password: 8+ characters, at least one special character and at least one number
    password_pattern = r'^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$'
    if not re.match(password_pattern, password):
        return "Password must be at least 8 characters long, have at least one special character and at least one number"

    # passed validation
    return 0

# messages in conversations
def validate_message(message):
    
    # allow messages that are from 1 to 500 characters long
    if not (1 <= len(message) < 500):
        return "Mesage can't be empty and can't be longer than 500 characters"
    
    # passed validation
    return 0

def validate_content(url_name, author, type, description):

    if Content.objects.filter(url_name=url_name).exists():
        return "Content with the specified title already exists in the database"

    # url_name is the title converted to lowercase and spaces replaced with dashes
    # only allow lowercase letters, numbers and dashes for the url_name
    url_name_pattern = r'^[a-z0-9-]{3,20}$'
    if not re.match(url_name_pattern, url_name):
        return "Title cannot contain any special characters"

    # only allow letters and numbers for the author's name
    author_pattern = r'^[a-zA-Z0-9\s]{3,20}$'
    if not re.match(author_pattern, author):
        return "Author's name cannot contain any special characters"

    if not len(url_name) > 1:
        return "Title is too short"
    
    if not len(url_name) < 50:
        return "Title is too long"
    
    if not len(author) > 1:
        return "Author's name is too short"
    
    if not len(author) < 50:
        return "Author's name is too long"

    if not len(description) > 5:
        return "Description is too short"
    
    if not len(description) < 2000:
        return "Description is too long"

    if not type in content_types:
        return "Specified content type is invalid"
    
    # passed validation
    return 0

def validate_review(content, summary, description, user, isEdit):

    if not len(summary) < 100:
        return "Summary is too long"
    
    if not len(summary) > 1:
        return "Summary is too short"
    
    if not len(description) < 2000:
        return "Review is too long"

    if not len(description) > 5:
        return "Review is too short"

    if not isEdit:
        try: 
            Review.objects.get(Q(author=user) & Q(content=content))
            return "You have already written a review for this content"
        except:
            return 0 # passed validation

    return 0 # passed validation