from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from system.models import SysMenu
from _overlapped import NULL


# Create your views here.
class MainView(TemplateView):
    ''' 
    main화면 
    '''
    print('==============MainView Class')
    template_name = 'main/main.html'
    
    @method_decorator(login_required)
    def get(self, request):
        print('================MainView-get')
        return render(request, 'main/main.html', {})  

    @method_decorator(login_required)
    def post(self, request):
        print('===========MainView-post')
        return render(request, 'main/main.html', {})     



@login_required(login_url='/accounts/login/')
def mainView(request):
    '''
    메인 화면 View(Function Based)
    '''
    print("view.mainView############################>")
    print("request.user" )
    print(request.user.userId)
    print(request.user.userNm)
    print(request.user.userAuth)
    print(request.user.userAuthNm())
    print("view.mainView############################<")
    
    # 메뉴 데이터 조회(사용중, 권한에 따른 세팅)
    menus = SysMenu.objects.filter(
        useYn__exact = True, 
        menuAuth__in = ['A', request.user.userAuth],
        menuLvl__exact = 3,
    ).order_by('upMenuId', 'menuId')
    
    # 템플릿 렌더링 및 데이터 전달
    return render(
        request, 
        'main/main.html', 
        {
            'menus' : menus,
        }
    )

@csrf_exempt
@login_required(login_url='/accounts/login/')
def contentsView(request):
    '''
    메뉴별 컨텐츠(right)
    '''
    contentsId =''
    try:
        if request.POST:
            menuUrl = request.POST.get('menuUrl')
            print("request.POST.get= {}".format(request.POST.get('menuUrl')))        
        else:
            if request.GET:
                menuUrl = request.GET.get('menuUrl')
                print("request.GET.get= {}".format(request.GET.get('menuUrl')))        
    
        # ID 를 이용한 SystemMenu를  조회 후 처리 추가 필요
        sysMenu = SysMenu.objects.filter()
    
        return render(request, 'main/contents/contents_' + contentsId + '.html', {'sysMenu': sysMenu})
    except Exception as err :
        print(err) 
        raise Http404



