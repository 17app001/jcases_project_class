from django.contrib import admin
from .models import City, Respondent, Profile
from django.contrib.auth.admin import UserAdmin
from .forms import ProfileForm

# Register your models here.
admin.site.register(City)
admin.site.register(Respondent)


class ProfileAdmin(UserAdmin):
    model=Profile
    add_form=ProfileForm
    filedsets=[
        *UserAdmin.fieldsets,
        [
            'User role',
            {
                'fields':[
                    'point','certification','city','respondent'
                ]
            }
        ]
    ]

admin.site.register(Profile,ProfileAdmin)