from django.contrib import admin
from .models import * 
# Register your models here.
admin.site.register(Category)
admin.site.register(Amount)
admin.site.register(State)
admin.site.register(Mode)
admin.site.register(Period)
admin.site.register(Case)

