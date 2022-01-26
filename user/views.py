from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
# Create your views here.


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('login')


def user_login(request):
    username, password = '', ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user)  # request.user
            return redirect('cases')

        print('登入失敗!')

    return render(request, './user/login.html', {'username': username, 'password': password})
