from django.shortcuts import redirect, render
from .models import Case
from .forms import CreateCaseForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.

def case(request,id):
    case=Case.objects.get(id=id)
    case.view+=1
    case.save()

    response= render(request,'./case/case.html',{'case':case})
    response.set_cookie('page','case')

    return response

@login_required(login_url='login')
def update_case(request,id):
    page=request.COOKIES.get('page')
    case=Case.objects.get(id=id)

    if request.method=='GET':
        form=CreateCaseForm(instance=case)

    if request.method=='POST':
        case.updatedon=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        form=CreateCaseForm(request.POST,instance=case)
        if form.is_valid():
            form.save()

            if page=='case':
                return redirect('case',id=case.id)

            return redirect('profile',id=request.user.id)

    return render(request,'./case/update-case.html',{'form':form,'page':page})

@login_required(login_url='login')
def delete_case(request,id):
    page=request.COOKIES.get('page')
    case=Case.objects.get(id=id)
    
    if request.method=='POST':   
        if request.POST.get('confirm'):
            case.delete()
            if page=='case':
                return redirect('cases')

        if request.POST.get('cancel'):
            if page=='case':
                return redirect('case',id=case.id)

        return redirect('profile',request.user.id)

    return render(request,'./case/delete-case.html',{'case':case})

@login_required(login_url='login')
def create_case(request):
    if request.method=='GET':
        form=CreateCaseForm()

    if request.method=='POST':
        form=CreateCaseForm(request.POST)
        if form.is_valid():
            case=form.save(commit=False)
            #指定使用者
            case.owner=request.user
            case.save()
            #儲存多對多關係
            form.save_m2m()

            return redirect('cases')
        

    return render(request,'./case/create-case.html',{'form':form})

def cases(request):
    cases = Case.objects.all()   

    return render(request, './case/cases.html', {'cases': cases})
