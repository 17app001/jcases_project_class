from django.shortcuts import redirect, render
from .models import Case, Category
from user.models import City
from .forms import CreateCaseForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .utils import search_cases,get_page_object,PAGE_NUM
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
    categorys=Category.objects.all() 
    countys=City.objects.all()

    category_id=request.COOKIES.get('category_id',0)
    county_id=request.COOKIES.get('county_id',0)
    search=request.COOKIES.get('search','').encode('iso-8859-1').decode('utf-8')

    category_id=category_id if category_id==0 else eval(category_id)
    county_id=county_id if county_id==0 else eval(county_id)

    if request.method=='GET':
        page_number = request.GET.get('page')
        # cases = cases=search_cases(category_id,county_id,search)  

    if request.method=='POST':
        page_number = 1
        category_id=eval(request.POST.get('category')) if request.POST.get('category') else 0
        county_id=eval(request.POST.get('county')) if request.POST.get('county') else 0      
        search=request.POST.get('search')

    cases=search_cases(category_id,county_id,search)
 
      
    page_num=PAGE_NUM
    page_obj = get_page_object(cases,page_number,page_num)

    context={'cases': cases,'categorys':categorys,
    'countys':countys,'category_id':category_id,
    'county_id':county_id,'search':search,'page_obj': page_obj,'cases_length':len(cases)}

    response =render(request, './case/cases.html', context=context)

    if request.method=='POST':
        response.set_cookie('category_id',category_id)
        response.set_cookie('county_id',county_id)
        response.set_cookie('search',bytes(search,'utf-8').decode('iso-8859-1'))


    return response


def index(request):
    categorys=Category.objects.all() 
    countys=City.objects.all()
    category_id,county_id,search=0,0,''
    page_number = request.GET.get('page')
    cases=search_cases(category_id,county_id,search)     
    page_num=PAGE_NUM
    page_obj = get_page_object(cases,page_number,page_num)

    context={'cases': cases,'categorys':categorys,
    'countys':countys,'category_id':category_id,
    'county_id':county_id,'search':search,'page_obj': page_obj,'cases_length':len(cases)}

    response =render(request, './case/cases.html', context=context)
    response.delete_cookie('category_id')
    response.delete_cookie('county_id')
    response.delete_cookie('search')

    return response