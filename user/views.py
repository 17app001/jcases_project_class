from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from case.utils import search_cases,get_page_object,PAGE_NUM
# Create your views here.

@login_required(login_url='login')
def profile(request,id):
    user=Profile.objects.get(id=id)
    cases=user.case_set.all()
    page_num=PAGE_NUM
    page_number = request.GET.get('page')
    page_obj = get_page_object(cases,page_number,page_num)
       
    response=render(request,'./user/profile.html',{'user':user,'page_obj':page_obj})
    response.set_cookie('page','profile')

    return response

def user_register(request):    
    if request.method=='GET':
        form=ProfileForm()

    elif request.method=='POST':
        print(request.POST)
        form=ProfileForm(request.POST)

        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()

            login(request, user)  # request.user
            return redirect('cases')


    return render(request,'./user/register.html',{'form':form})

@login_required(login_url='login')
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
