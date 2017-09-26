import datetime
from io import StringIO
import json

from django.conf import settings
from django.core.serializers.json import Serializer

from utils.data import is_empty


class JSONSerializer(Serializer):
    '''
    JSON serialize to serialize db fields and properties

    Example:
    >>> JSONSerializer().serialize(Model.objects.all(), ('field1', 'field2',))
    '''
    def serialize(self, queryset, attributes, **options):
        self.options = options
        self.stream = options.get("stream", StringIO())
        self.start_serialization()
        self.first = True

        for obj in queryset:
            self.start_object(obj)
            for field in attributes:
                self.handle_field(obj, field)
            self.end_object(obj)
            if self.first:
                self.first = False
        self.end_serialization()
        return self.getvalue()

    def handle_field(self, obj, field):
        self._current[field] = getattr(obj, field)


def jsonDefault(value):
    '''
    json Datetime 변환용
    '''
    if isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d %H:%M:%S')

    raise TypeError('not JSON serializable')

def makeJsonResult(result=True, resultMessage=None, form=None, resultData=None,):
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


#def makeJsonDump(result=True, resultMessage=None, form=None, resultData=None):
def makeJsonDump(result=True, resultMessage=None, form=None, resultData=None, maskYn=False, maskFields=None):
    '''
    json결과 세팅
    '''
    jsonData = {}
    resultCode = "OK" if result else "NG"
    errorItem = ""

    # From 데이터가 있는 경우
    if form is not None:
        if len(form.errors) == 0:
            resultCode = "OK"
        else:
            errorItem = list(form.errors.keys())[0]
            resultMessage = form[errorItem].errors.as_text().replace("* ", "\n")
            resultCode = "NG"

    # 데이터 마스킹 처리
    if not is_empty(resultData) and maskYn and not is_empty(maskFields):
        for data in resultData:
            for keyField, valType in maskFields.items():
                data[keyField] = masking_data(data[keyField], valType)

    # 결과 코드 세팅
    jsonData['resultCode'] = resultCode
    jsonData['resultMessage'] = resultMessage if resultMessage is not None else ""
    jsonData['resultData'] = resultData if resultData is not None else {}
    jsonData['errorItem'] = errorItem

    jsonDumps = json.dumps(
        jsonData,
        default=jsonDefault,
        indent=2,
    )

    # Json 데이터 확인
    if settings.DEBUG:
        print(jsonDumps)

    return jsonDumps


def masking_data(data=None, maskType=None):
    '''
    데이터 마스킹 처리
    '''
    if is_empty(data) or is_empty(maskType):
        return data

    if maskType == "T":  # 전화번호
        data = masking_tel_no(data)
    elif maskType == "N":  # 이름
        data = masking_name(data)
    elif maskType == "I":  # 아이디
        data = masking_id(data)
    else:
        pass

    return data


def masking_tel_no(data=None):
    '''
    전화번호 마스킹 처리
    '''
    if not is_empty(data) and len(data) > 0:
        data = data[:1].ljust(4, "*")
    return data


def masking_name(data):
    '''
    이름 마스킹 처리
    '''
    if not is_empty(data) and len(data) > 0:
        data = data[:1].ljust(len(data), "*")
    return data


def masking_id(data):
    '''
    아이디 마스킹 처리
    '''
    if not is_empty(data) and len(data) > 0:
        data = data[:2].ljust(4, "*") + data[-2:]
    return data
