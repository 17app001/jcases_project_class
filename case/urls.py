from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cases,name='cases'),
    path('create-case/', views.create_case,name='create-case'),
    path('case/<str:id>', views.case, name='case'),
    path('delete-case/<str:id>', views.delete_case, name='delete-case'),
    path('update-case/<str:id>', views.update_case, name='update-case'),

]
