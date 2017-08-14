from datetime import datetime
import re

from django.db.models.expressions import F
from django.db.models.query_utils import Q

from common.models import ComCd
from system.models import SysSeq, SysShop
from system.models import SysUser, SysAppreq
from utils.const import NTEL_EXCLUDE_IDS


def getComCdList(grpCd=None, useYn=True, grpOpt=None, orderOpt=''):
    '''공통코드 조회 리스트
    '''
    # 조회 쿼리 조건
    qry = Q()

    # 그룹코드
    qry &= Q(grpCd__exact=grpCd)

    # 사용여부
    if useYn:
        qry &= Q(useYn__exact=useYn)

    # 그룹옵션
    if grpOpt:
        qry &= Q(grpOpt__contains=grpOpt)

    comCds = ComCd.objects.filter(
        qry
    ).order_by(
        orderOpt + "ordSeq"
    )

    return comCds


def getSysSeqId(seqCd):
    '''
    시스템 Seq 코드 획득(seqCd별)
    seqCd는 sys_seq 테이블 값 참조
    '''
    returnCd = None

    # SysSeq에서 해당SEQ 코드의 데이터를 획득
    sysSeq = SysSeq.objects.filter(
        seqCd__exact=seqCd,
        useYn__exact=True,
    )

    # 해당 SEQ Code에 대한 값이 없을 경우
    if sysSeq is None:
        return returnCd

    seq = sysSeq.get().seq  # 현재 seq 값을 획득
    seqPrefix = sysSeq.get().seqPrefix  # prefix 값을 획득
    useYm = sysSeq.get().useYm  # 년월 사용여부
    seqYm = str(datetime.today().strftime("%y%m")) if useYm else ""

    seqLen = sysSeq.get().seqLen  # seq length 값을 획득
    seqPrefixLen = len(seqPrefix)  # prefix 길이
    seqYmLen = len(seqYm)  # prefix 길이

    returnCd = seqPrefix + seqYm + str(seq).zfill(seqLen - seqPrefixLen - seqYmLen)

    sysSeq.update(
        seq=F('seq') + 1
    )
    return returnCd


def isUsableId(userId):
    '''
    사용가능한 사용자아이디 체크
    '''
    # 아이디 조합이 올바른지 확인(영문으로 시작하며 영숫자 조합 6자리 이상인가)
    if not re.match(r'^([a-zA-Z])[a-zA-Z\d]{5,19}$', str(userId)):
        return False

    # 금기어가 포함되었는지 아닌지 확인
    for excludeWord in NTEL_EXCLUDE_IDS:
        if excludeWord in str(userId):
            return False
        else:
            pass

    # 사용자 정보(SysUser)에서 중복 확인
    qry = Q()
    qry &= Q(userId__exact=userId)
    sysUser = SysUser.objects.filter(
        qry
    ).first()

    if sysUser is None:
        # 이용신청(SysAppreq)에 등록된 ID 중복 확인
        userAppreq = SysAppreq.objects.filter(
            qry
        ).first()

        if userAppreq is None:
            return True
        else:
            return False
    else:
        return False


def getShopList(companyId=None, shopId=None, shopOnly=True, useYn=True):
    '''
     소속 매장 목록 데이터 획득
    '''
    qry = Q()
    # 사용여부 조건
    if useYn:
        qry &= Q(useYn__exact=useYn)
    # 대상 매장 조건
    if shopOnly:
        qry &= Q(shopId__exact=shopId)
    else:
        qry &= Q(shopId__companyId__exact=companyId)
    shopList = SysShop.objects.filter(
        qry
    ).order_by(
        "shopId",
    )
    return shopList
