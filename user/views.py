from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from .models import Profile
# Create your views here.


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('login')


def user_login(request):
    username, password,message = '', '',''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)
        user = authenticate(request, username=username, password=password)
        # print(user)
        if user:
            login(request, user)  # request.user
            return redirect('cases')

        #帳號錯誤
        if Profile.objects.filter(username=username).exists():
            message='密碼錯誤'
        else:
            message='帳號錯誤'


    return render(request, './user/login.html', {'username': username, 'password': password,
    'message':message})
