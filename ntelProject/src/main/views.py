from django.contrib.auth.decorators import login_required
from django.db.models.query import Prefetch
from django.http.response import Http404
from django.shortcuts import render
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
def mainView(request):
    '''
    메인 화면 View(Function Based)
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



