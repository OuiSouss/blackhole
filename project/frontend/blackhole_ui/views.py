from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.shortcuts import render

def index(request):
    if request.user.is_authenticated:
        #return HttpResponse("Gestion des routes")

        #template = loader.get_template('templates/route_manager.html')
        #return HttpResponse(template.render())
        #return render(request, 'templates/route_manager.html', context)

        return render(request,'route_dashboard/route_dashboard.html')
    
    else:
        return redirect('/accounts/login/')
