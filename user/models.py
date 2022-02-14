from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import SET_NULL
# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Respondent(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Profile(AbstractUser):
    email=models.EmailField(unique=True,null=False)
    point = models.IntegerField(default=0)
    certification = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=SET_NULL, null=True)
    respondent = models.ForeignKey(Respondent, on_delete=SET_NULL, null=True)

    def __str__(self):
        return self.username
