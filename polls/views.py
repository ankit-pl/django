"""Module docstring"""

from django.shortcuts import render
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required

# @login_required(login_url='http://localhost:8000/accounts/login')
def index(request):
    """Function docstring"""
    return render(request, 'polls/home.html')