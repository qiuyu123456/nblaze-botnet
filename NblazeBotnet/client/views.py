from django.shortcuts import render,redirect
from client.models import Client
from client.models import client_setting


# Create your views here.
def update_version(request):
    data = client_setting.objects.get(id=1)
    return render(request, 'update_version.html',{"data":data})


def index(request):
    client_data = Client.objects.all()
    return render(request, 'index.html', {'client_data': client_data})


def client_set(request):
    set_data = client_setting.objects.get(id=1)
    return render(request, 'client_setting.html', {'set_data': set_data})


def update_client_set(request):
    ip = request.POST.get('ip')
    port = request.POST.get('port')
    version = request.POST.get('version')
    status = request.POST.get('status')
    set_data = client_setting.objects.get(id=1)
    set_data.ip = ip
    set_data.port = port
    set_data.version = version
    set_data.status = status
    set_data.save()
    return redirect('/client_setting')
