import django
from django.shortcuts import redirect, render
from .models import Case, Category
from user.models import City
from .forms import CreateCaseForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q
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
    category_id,county_id,search=0,0,''
    categorys=Category.objects.all() 
    countys=City.objects.all()

    if request.method=='GET':
        cases = Case.objects.all()  

    if request.method=='POST':
        category_id=eval(request.POST.get('category')) if request.POST.get('category') else 0
        county_id=eval(request.POST.get('county')) if request.POST.get('county') else 0      
        search=request.POST.get('search')

        category_q=Q(category_id=category_id)
        county_q= Q(owner__city_id=county_id)
        search_q=Q(title__contains=search) | Q(description__contains=search)

        print(category_q,county_q,search_q)

        if category_id and county_id:
            cases=Case.objects.filter(category_q & county_q & search_q) if search else\
                 Case.objects.filter(category_q & county_q)       
        elif category_id:
            cases=Case.objects.filter(category_q & search_q) if search else\
                Case.objects.filter(category_q)
        elif county_id:
            cases=Case.objects.filter(county_q & search_q) if search else\
                Case.objects.filter(county_q)
        elif search:
             cases=Case.objects.filter(search_q)        
        else:
            cases = Case.objects.all()       
    
    print(cases)
    return render(request, './case/cases.html', {'cases': cases,'categorys':categorys,
    'countys':countys,'category_id':category_id,'county_id':county_id,'search':search})
