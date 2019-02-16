from django.urls import path
from . import views

urlpatterns = [
    path('q/', views.search, name='search_question'),
]
