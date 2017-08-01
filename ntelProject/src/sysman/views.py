from __future__ import absolute_import

from django.shortcuts import render

from utils.ajax import login_required_ajax


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
