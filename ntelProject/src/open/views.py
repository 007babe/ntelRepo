from __future__ import absolute_import

from django.shortcuts import render
from common.utils.ajax import login_required_ajax


@login_required_ajax
def openNewTab1CV(request):
    '''
    개통업무 > 신규개통 : 단말기 컨텐츠
    '''
    return render(
        request,
        'open/new/contents_tab1.html',
        {},
    )


@login_required_ajax
def openNewTab2CV(request):
    '''
    개통업무 > 신규개통 : 유심/중고 컨텐츠
    '''
    return render(
        request,
        'open/new/contents_tab2.html',
        {},
    )


@login_required_ajax
def openNewTab3CV(request):
    '''
    개통업무 > 신규개통 : 홈상품 컨텐츠
    '''
    return render(
        request,
        'open/new/contents_tab3.html',
        {},
    )
