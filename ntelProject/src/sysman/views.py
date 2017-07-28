from common.utils.ajax import login_required_ajax
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from system.models import SysMenu


@login_required_ajax
def sysmanUseTab1CV(request):
    '''
    시스템관리 > 사용관리  : 사용회사 컨텐츠
    '''
    return render(
        request, 
        'sysman/use/contents_tab1.html', 
        {},
    )

@login_required_ajax
def sysmanUseTab2CV(request):
    '''
    시스템관리 > 사용관리  : 사용자 컨텐츠
    '''
    return render(
        request, 
        'sysman/use/contents_tab2.html', 
        {},
    )

