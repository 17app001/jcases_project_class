from django.shortcuts import redirect, render
from .models import Case
from user.models import Profile
from .forms import CreateCaseForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def case(request,id):
    case=Case.objects.get(id=id)
    case.view+=1
    case.save()

    return render(request,'./case/case.html',{'case':case})

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
