from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.shortcuts import render
import requests
import json
from route_manager.forms import PostForm

def index(request):
    if request.user.is_authenticated:
        response = requests.get('http://127.0.0.1:5000/api/subnet')
        json_data = response.json()
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                route = form.save(commit=False)
                print (route.ip)
                print (route.next_hop)
                print (route.community)
                
        else:
            form = PostForm()

        
        return render(request, 'route_dashboard/route_dashboard.html', {
            'data' : json_data,
            'form': form,
        })
    else:
        return redirect('/accounts/login/')





