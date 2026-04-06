from django.shortcuts import render
from .models import Part

def part_list(request):
    parts = Part.objects.all()
    return render(request, 'inventory/part_list.html', {'parts': parts})
