from django.urls import path
from . import views

urlpatterns = [
    path('q/', views.search, name='search_question'),
    path('login/', views.login, name='loginme'),
    path('auth/', views.authenticate, name='authentication'),
    path('getq/', views.getQ, name='Get Queries'),
    path('getqid/', views.getQID, name='Get QID'),
    path('getf/', views.getF, name='Get Frequencies'),
    path('setf/', views.setF, name='Set Frequencies'),
    path('preferences/', views.pref_update, name='Preferences'),
    path('updated/', views.updated, name='Thank you')
]
