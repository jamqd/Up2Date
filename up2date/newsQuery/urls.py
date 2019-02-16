from django.urls import path
from . import views

urlpatterns = [
    path('q/', views.search, name='search_question'),
    path('login/', views.login, name='loginme'),
    path('auth/', views.authenticate, name='authentication'),
    path('preferences/', views.pref_update, name='Preferences'),
    path('updated/', views.updated, name='Thank you')
]
