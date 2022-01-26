from django.shortcuts import render
from .models import Case
from user.models import Profile

# Create your views here.


def cases(request):
    cases = Case.objects.all()   

    return render(request, './case/cases.html', {'cases': cases})
