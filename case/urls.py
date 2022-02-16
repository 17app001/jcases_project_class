from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cases,name='cases'),
    path('create-case/', views.create_case,name='create-case'),
    path('case/<str:id>', views.case, name='case'),

]
