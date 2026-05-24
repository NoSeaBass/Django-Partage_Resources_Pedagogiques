from django.urls import path
from . import views

app_name = 'utilisateurs'

urlpatterns = [
    path('inscription/', views.inscription_etudiant, name='inscription_etudiant'),
]
