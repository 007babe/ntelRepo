import datetime


def jsonDefault(value):
    '''
    json Datetime 변환용
    '''
    if isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    raise TypeError('not JSON serializable')


def makeJsonResult(result=True, resultMessage=None, form=None, resultData=None):
    '''
    json결과 세팅
    '''
    jsonData = {}
    resultCode = "OK" if result else "NG"
    errorItem = ""

    # 에러 데이터가 있을 경우
    if form is not None:
        if len(form.errors) == 0:
            resultCode = "OK"
        else:
            errorItem = list(form.errors.keys())[0]
            resultMessage = form[errorItem].errors.as_text().replace("* ", "\n")
            resultCode = "NG"

    # 결과 코드 세팅
    jsonData['resultCode'] = resultCode
    jsonData['resultMessage'] = resultMessage if resultMessage is not None else ""
    jsonData['resultData'] = resultData if resultData is not None else {}
    jsonData['errorItem'] = errorItem

    return jsonData
