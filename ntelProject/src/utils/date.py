import datetime

from keyczar.keyczar import Crypter

from config import settings


def getltdt(strDt=None):
    '''
    날짜 __lt 사용시 1일 Plus
    '''
    try:
        ltdt = datetime.datetime.strptime(strDt, "%Y-%m-%d") + datetime.timedelta(days=1)
    except:
        return strDt

    return ltdt


def masking_data(data=None, maskingYn=True, encyptYn=False):
    '''
    데이터 마스킹 처리
    '''
    print(data, type(data))

    if data is not None and maskingYn:
        # 암호화 데이터 일 경우 복호화 처리
        if encyptYn:
            crypter = Crypter.Read(settings.ENCRYPTED_FIELDS_KEYDIR)
            data = crypter.Decrypt(data)

    return "aaab"
#    return data
