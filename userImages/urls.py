from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('showImage/', views.showImage, name='showimage'),
    path('addImage/', views.addImage),
    path('checkFaceEmbedding/', views.checkFaceEmbedding)
]