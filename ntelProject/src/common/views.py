from __future__ import absolute_import

import json

from django.shortcuts import render


def errorPopupCV(request):
    '''
    공통 Error 팝업
    '''
    return render(
        request,
        'common/errors/errorPopup.html',
        {}
    )

