# -*- coding: utf-8 -*-
# Create your views here.
'''
메인화면 
'''

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


@login_required(login_url='/accounts/login/')
def mainView(request):
    return render(request, 'main/main.html', {})
