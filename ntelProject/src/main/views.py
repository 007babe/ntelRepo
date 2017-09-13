from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.http.response import Http404, HttpResponse
from django.middleware import csrf
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.urls.base import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from system.forms import SysUserChangeShopForm
from system.models import SysMenu, SysShop, SysCompanyAccount, SysUser
from utils.ajax import login_required_ajax, login_required_ajax_post
from utils.data import is_empty
from utils.json import makeJsonDump


class MainView(TemplateView):
    '''
    main화면
    사용안함
    '''
    template_name = 'main/main.html'

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'main/main.html', {})

    @method_decorator(login_required)
    def post(self, request):
        return render(request, 'main/main.html', {})


@login_required(login_url=reverse_lazy("logins:login"))
def mainCV(request):
    '''
    메인 화면
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    # 매장 정보 획득
    userShops = None
    if userAuth in ["S0001M", "S0001C", "S0001A"]:  # 시스템관리자, 대표, 총괄 일 경우 가능
        userShops = SysShop.objects.for_company(
            useYn=True,
            companyId=request.user.orgShopId.companyId
        )
    else:
        userShops = SysShop.objects.for_shop(
            useYn=True,
            shopId=request.user.orgShopId
        )

    # 템플릿 렌더링 및 데이터 전달
    return render(
        request,
        'main/main.html',
        {
            "userShops": userShops,  # 사용자의 매장 정보
        }
    )


@login_required_ajax
def menuCV(request):
    '''
    메뉴별 초기화면 Contents View(Function Based)
    '''
    try:
        # 메뉴ID(Key)로 메뉴 정보 획득
        sysMenuInfo = SysMenu.objects.get(
            menuId__exact=request.POST.get('menuId'),
        )

        # 템플릿 렌더링 및 데이터 전달
        return render(
            request,
            sysMenuInfo.menuTmp,
            {
                'naviMenu': sysMenuInfo,
            }
        )
    except TemplateDoesNotExist:  # Template이 존재하지 않을 경우
        print("menuCV :: 템플릿이 존재하지 않음 [%s]" % sysMenuInfo.menuTmp)
        raise Http404


@login_required_ajax_post
def jsonChangeShop(request):
    '''
    환경설정 >  거래처관리  : 리스트 데이터 Json
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A"]:  # 시스템관리자, 대표, 총괄만 가능
        # 수정할 데이터 획득
        userInfo = SysUser.objects.for_company(
            companyId=request.user.orgShopId.companyId,
        ).get(
            userId__exact=request.user
        )

        # 직원정보 수정 폼
        sysUserChangeShopForm = SysUserChangeShopForm(
            request.POST,
            instance=userInfo,
            request=request,
        )

        # 데이터 검증 후 저장
        if sysUserChangeShopForm.is_valid():
            sysUserChangeShopForm.save()

        return HttpResponse(
            makeJsonDump(
                form=sysUserChangeShopForm,
            ),
            content_type="application/json",
        )
    else:
        raise PermissionDenied()

