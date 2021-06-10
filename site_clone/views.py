from django.shortcuts import redirect
from django.conf import settings


def home(request):
    return redirect('news/')
