from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    """Activity Management System - Main Dashboard"""
    context = {
        'page_title': 'Activity Management System',
        'app_name': 'WDAMMS - Western Dart Activity Management & Monitoring System'
    }
    return render(request, 'wdamms/index.html', context)
