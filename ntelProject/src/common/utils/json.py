import datetime


def jsonDefault(value): 
    '''
    json Datetime 변환용
    '''
    if isinstance(value, datetime.date): 
        return value.strftime('%Y-%m-%d %H:%M:%S') 
    raise TypeError('not JSON serializable')