from __future__ import absolute_import

import json

from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.http import HttpResponse

from system.models import SysMenu, SysUser, SysCompany, SysMsg
from utils.ajax import login_required_ajax
from utils.json import jsonDefault
from utils.json import makeJsonResult


@login_required_ajax
def getJsonSysMenu(request):
    """
    사용자메뉴(sys_menu) 데이터 획득(Json)
    """
    #######################################
    # Query 시스템 사용자별 메뉴 데이터 획득
    #######################################
    # sysMenu
    qry = Q(useYn__exact=True)  # 사용여부
    qry &= Q(menuLvl__exact=3)  # 레벨 3
    # sysMenuAuth
    qry &= Q(r_system_sysmenuauth_menu_id__useYn__exact=True)  # 사용여부
    qry &= Q(r_system_sysmenuauth_menu_id__menuAuth__exact=request.user.userAuth)  # 사용자 권한
    # SysMenuCompayTp
    qry &= Q(r_system_sysmenucompanytp_menu_id__useYn__exact=True)  # 사용여부
    qry &= Q(r_system_sysmenucompanytp_menu_id__companyTp__exact=request.user.shopId.companyId.companyTp)  # 사용자 권한

    sysMenus = SysMenu.objects.filter(
        qry
    ).order_by(
        'upMenuId',
        'menuId',
    ).annotate(
        upMenuNm=F('upMenuId__menuNm'),
        upMenuCss=F('upMenuId__menuCss'),
        topMenuNm=F('upMenuId__upMenuId__menuNm'),
    ).values(
        'menuId',
        'menuNm',
        'menuTmp',
        'menuCss',
        'upMenuId',
        'upMenuNm',
        'upMenuCss',
        'topMenuNm',
    )

    return HttpResponse(
        json.dumps(
            makeJsonResult(
                resultData=list(sysMenus)
            ),
            default=jsonDefault
        ),
        content_type="application/json"
    )


def getJsonSysMsg(request):
    """
        시스템메세지(sys_msg) 데이터 획득(Json)
    """
    # Query 조합
    qry = Q()

    sysMsgs = SysMsg.objects.filter(
        qry
    ).annotate(
        msgType=F('msgTp__comNm'),
    ).values(
        'msgCd',
        'msgType',
        'title',
        'msg',
        'useYn',
    )

    return HttpResponse(
        json.dumps(
            makeJsonResult(
                resultData=list(sysMsgs)
            ),
            default=jsonDefault
        ),
        content_type="application/json"
    )


@login_required_ajax
def getJsonSysCompany(request):
    """
        시스템회사(sys_company) 데이터 획득(Json)
    """
    #######################################
    # Query 시스템 사용자별 메뉴 데이터 획득
    #######################################
    # sysMenu
    qry = Q()
    '''
    qry &=  Q(useYn__exact=True)  # 사용여부
    qry &= Q(menuLvl__exact=3)  # 레벨 3
    # sysMenuAuth
    qry &= Q(r_system_sysmenuauth_menu_id__useYn__exact=True)  # 사용여부
    qry &= Q(r_system_sysmenuauth_menu_id__menuAuth__exact=request.user.userAuth)  # 사용자 권한
    # SysMenuCompayTp
    qry &= Q(r_system_sysmenucompanytp_menu_id__useYn__exact=True)  # 사용여부
    qry &= Q(r_system_sysmenucompanytp_menu_id__companyTp__exact=request.user.shopId.companyId.companyTp)  # 사용자 권한
    '''
    sysCompanys = SysCompany.objects.filter(
        qry
    ).order_by(
        'companyId',
    ).annotate(
        companyTpNm=F('companyTp__comNm'),
        companyGradeNm=F('companyGrade__comNm'),
        regNm=F('regId__userNm'),
        modNm=F('modId__userNm'),
    ).values(
        'companyId',
        'companyNm',
        'companyTp',
        'companyTpNm',
        'companyGrade',
        'companyGradeNm',
        'telNo',
        'cellNo',
        'zipCd',
        'addr1',
        'addr2',
        'useYn',
        'regDt',
        'regId',
        'regNm',
        'modDt',
        'modId',
        'modNm',
    )

    return HttpResponse(
        json.dumps(
            makeJsonResult(
                resultData=list(sysCompanys)
            ),
            default=jsonDefault
        ),
        content_type="application/json"
    )


@login_required_ajax
def getJsonShopStaff(request):
    """
        매장직원데이터(sys_user) 데이터 획득(Json)
    """
    #######################################
    # Query 매장 직원 데이터 획득
    #######################################
    qry = Q(useYn__exact=True)  # 사용여부
    qry &= Q(shopId__exact=request.user.shopId)  # 사용자 해당 매장ID

    shopStaffs = SysUser.objects.filter(
        qry
    ).values()

    return HttpResponse(
        json.dumps(
            makeJsonResult(
                resultData=list(shopStaffs)
            ),
            default=jsonDefault
        ),
        content_type="application/json"
    )
