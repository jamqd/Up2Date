from django.urls import path
from . import views

urlpatterns = [
    path('q/', views.search, name='search_question'),
    path('preferences/', views.pref_update, name='Preferences'),
    path('updated/', views.updated, name='Thank you')
]
