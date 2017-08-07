from __future__ import absolute_import

from django.views.generic.base import TemplateView


# Create your views here.
class IndexView(TemplateView):
    '''
    엔텔 Home Index
    '''
    template_name = 'index.html'
