from __future__ import absolute_import
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from common.utils.ajax import login_required_ajax
from system.models import SysMenu


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


@login_required(login_url='/logins/login')
def mainCV(request):
    '''
    메인 화면
    '''
    # 템플릿 렌더링 및 데이터 전달
    return render(
        request,
        'main/main.html',
        {}
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
        raise Http404
