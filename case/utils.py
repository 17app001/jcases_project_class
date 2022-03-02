
from django.db.models import Q
from .models import Case
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

PAGE_NUM=20

def search_cases(category_id,county_id,search=''):
    category_q=Q(category_id=category_id)
    county_q= Q(owner__city_id=county_id)
    search_q=Q(title__contains=search) | Q(description__contains=search)

    cases=None
    try:
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
    except Exception as e:
        print(e)
      
    return cases    


def get_page_object(cases, page, page_num):
    # 每次固定顯示幾筆資料
    paginator = Paginator(cases, page_num)
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return page_obj

