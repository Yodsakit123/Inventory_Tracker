from django.shortcuts import render
from .models import Part

# Import dash apps to register them with django-plotly-dash
from . import dash_apps

def part_list(request):
    parts = Part.objects.all()
    return render(request, 'inventory/part_list.html', {'parts': parts})

def dashboard(request):
    return render(request, 'inventory/dashboard.html')
