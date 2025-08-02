from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'wms/index.html')

def create_warehouse(request):
    if request.method == 'POST':
        return HttpResponse("Warehouse created successfully.")
    return render(request, 'wms/create_warehouse.html')
