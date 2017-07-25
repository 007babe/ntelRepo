from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from system.models import SysMenu

@login_required(login_url='/accounts/login/')
def openNewTab1CV(request):
    '''
    개통업무 > 신규개통 : 단말기 컨텐츠
    '''
    return render(
        request, 
        'open/new/contents_tab1.html', 
        {},
    )

@login_required(login_url='/accounts/login/')
def openNewTab2CV(request):
    '''
    개통업무 > 신규개통 : 유심/중고 컨텐츠
    '''
    return render(
        request, 
        'open/new/contents_tab2.html', 
        {},
    )

@login_required(login_url='/accounts/login/')
def openNewTab3CV(request):
    '''
    개통업무 > 신규개통 : 홈상품 컨텐츠
    '''
    return render(
        request, 
        'open/new/contents_tab3.html', 
        {},
    )
