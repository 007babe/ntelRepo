# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
'''
메인화면 
'''
def index(request):
    return render(request, 'main/main.html', {})
