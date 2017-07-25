from django.contrib.auth.decorators import login_required
from django.db.models.query import Prefetch
from django.http.response import Http404
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from system.models import SysMenu


# Create your views here.
class MainView(TemplateView):
    ''' 
    main화면 
    사용안함
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
def mainCV(request):
    '''
    메인 화면 Contents View(Function Based)
    '''
    '''
    print("view.mainView############################>")
    print("request.user" )
    print(request.user.userId)
    print(request.user.userNm)
    print(request.user.userAuth)
    print(request.user.userAuthNm())
    print("view.mainView############################<")
    print("view.mainView.userAuth############################<")
    print(request.user.userAuth)
    print(request.user.shopId.companyId.companyTp)
    print("view.mainView.userAuth############################<")
    '''
    
    '''
    # 메뉴 데이터 조회(사용중, 권한에 따른 세팅)
    menus = SysMenu.objects.filter(
        useYn__exact = True, 
        menuLvl__exact = 3,
        # SysMenuAuth
        r_system_sysmenuauth_menu_id__useYn__exact = True,
        r_system_sysmenuauth_menu_id__menuAuth__exact = request.user.userAuth,
        # SysMenuCompanyTp
        r_system_sysmenucompanytp_menu_id__useYn__exact = True,
        r_system_sysmenucompanytp_menu_id__companyTp__exact = request.user.shopId.companyId.companyTp,
    ).order_by(
        'upMenuId',
        'menuId'
    )
    '''
    
    # 템플릿 렌더링 및 데이터 전달
    return render(
        request, 
        'main/main.html', 
        {}
    )

@login_required(login_url='/accounts/login/')
def menuCV(request):
    '''
    메뉴별 초기화면 Contents View(Function Based)
    '''
    try :
        '''
        Parameter Check
        '''
        # POST
        print("Params:POST===============>")
        print("menuIdP : %s"  %request.POST.get('menuIdP'))
        print("menuId : %s"  %request.POST.get('menuId'))
        print("Params:POST===============<")
        # GET
        print("Params:GET===============>")
        print("menuIdP : %s"  %request.GET.get('menuIdP'))
        print("menuId : %s"  %request.GET.get('menuId'))
        print("Params:GET===============<")
        
        # 메뉴ID(Key)로 메뉴 정보 획득
        sysMenuInfo = SysMenu.objects.get(
            menuId__exact = request.GET.get('menuId'),
        )
        
        # 템플릿 렌더링 및 데이터 전달
        return render(
            request, 
            sysMenuInfo.menuTmp, 
            {
                'naviMenu' : sysMenuInfo,
            }
        )
    except TemplateDoesNotExist: # Template이 존재하지 않을 경우
        raise Http404
        
        
        
            




