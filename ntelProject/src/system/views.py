from __future__ import absolute_import

import json

from django.http import HttpResponse

from system.models import SysMenu, SysUser, SysCompany, SysMsg, SysShop, \
    SysComCd, SysHttpStatus
from utils.ajax import login_required_ajax_post
from utils.json import makeJsonDump


@login_required_ajax_post
def getJsonSysComCd(request):
    """
    공통코드(com_cd) 데이터 획득(Json)
    """
    sysComCds = SysComCd.objects.as_list(useYn=True)

    return HttpResponse(
        makeJsonDump(
            resultData=sysComCds
        ),
        content_type="application/json"
    )


def getJsonSysHttpStatus(request):
    """
    Http Status(com_http_status) 데이터 획득(Json)
    """
    sysHttpStatuses = SysHttpStatus.objects.as_list(useYn=True)

    return HttpResponse(
        makeJsonDump(
            resultData=sysHttpStatuses
        ),
        content_type="application/json"
    )


@login_required_ajax_post
def getJsonSysMenu(request):
    """
    사용자메뉴(sys_menu) 데이터 획득(Json)
    """
    sysMenus = SysMenu.objects.as_list(
        userAuth=request.user.userAuth,
        companyTp=request.user.shopId.companyId.companyTp,
    )

    return HttpResponse(
        makeJsonDump(
            resultData=sysMenus
        ),
        content_type="application/json"
    )


@login_required_ajax_post
def getJsonSysMsg(request):
    """
        시스템메세지(sys_msg) 데이터 획득(Json)
    """
    sysMsgs = SysMsg.objects.as_list(useYn=True)

    return HttpResponse(
        makeJsonDump(
            resultData=sysMsgs
        ),
        content_type="application/json"
    )


@login_required_ajax_post
def getJsonSysCompany(request):
    """
    시스템회사(sys_company) 데이터 획득(Json)
    """
    sysCompanys = SysCompany.objects.as_list()

    return HttpResponse(
        makeJsonDump(
            resultData=sysCompanys
        ),
        content_type="application/json"
    )


@login_required_ajax_post
def getJsonSysShop(request):
    """
    권한에 따른 매장(sys_shop) 데이터 획득(Json)
    """
    sysShops = SysShop.objects.as_list_by_auth(
        userAuth=request.user.userAuth_id,
        companyId=request.user.shopId.companyId,
        shopId=request.user.shopId,
    )

    return HttpResponse(
        makeJsonDump(
            resultData=sysShops
        ),
        content_type="application/json"
    )


@login_required_ajax_post
def getJsonShopStaff(request):
    """
    매장직원데이터(sys_user) 데이터 획득(Json)
    """
    #######################################
    # Query 매장 직원 데이터 획득
    #######################################
    shopStaffs = SysUser.objects.as_list_staff_for_shop(
        useYn=True,
        shopId=request.user.shopId,
        userId=request.user.userId,
        userAuth=request.user.userAuth,
    )

    return HttpResponse(
        makeJsonDump(
            resultData=shopStaffs
        ),
        content_type="application/json"
    )
