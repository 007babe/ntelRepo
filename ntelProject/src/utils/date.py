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
