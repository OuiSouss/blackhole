from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.shortcuts import render
import requests
import json

def index(request):
    if request.user.is_authenticated:
        response = requests.get('http://127.0.0.1:5000/api/subnet')
        json_data = response.json()

        #return HttpResponse("Gestion des routes")
        #template = loader.get_template('templates/route_manager.html')
        #return HttpResponse(template.render())
        #return render(request, 'templates/route_manager.html', context)
        
        
        return render(request, 'route_dashboard/route_dashboard.html', {
            'data' : json_data,
        })
    else:
        return redirect('/accounts/login/')
