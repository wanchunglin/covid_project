from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('verify/', views.verify)
]