from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),

    path('conversations/', views.conversations, name='conversations'),
    path('conversations/sync', views.sync_conversation, name='sync_conversation'),
    path('conversations/send', views.send_conversation, name='send_conversation'),
    path('conversation/<str:recipient_name>', views.conversation, name='conversation'),

    path('content/', views.content, name='content'),

    path('login/', views.custom_login, name='custom_login'),
    path('register/', views.register, name='register')
]