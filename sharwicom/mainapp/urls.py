from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),

    path('conversations/', views.conversations, name='conversations'),
    path('conversations/sync', views.sync_conversation, name='sync_conversation'), # only handles AJAX requests
    path('conversations/search', views.search_conversations, name='search_conversations'), # only handles AJAX requests
    path('conversations/send', views.send_conversation, name='send_conversation'), # only handles AJAX requests
    path('conversations/request', views.request_conversation, name='request_conversation'), # only handles AJAX requests
    path('conversation/<str:recipient_name>', views.conversation, name='conversation'),

    path('rate-content/', views.rate_content, name='rate_content'), # only handles AJAX requests
    path('content/<str:content_url_name>', views.content, name='content'),
    path('add-content/', views.add_content, name='add_content'),
    path('add-review/<str:content_url_name>', views.add_review, name='add_review'),
    path('edit-review/<str:content_url_name>', views.edit_review, name='edit_review'),

    path('community/<str:community_url_name>', views.community, name='community'),

    path('login/', views.custom_login, name='custom_login'),
    path('register/', views.register, name='register')
]