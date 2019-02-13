from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.conf import settings
from requests.exceptions import ConnectionError
import requests

from route_manager.forms import PostForm




#VERIFIE L'AUTHENTIFICATION
def not_auth(request):
    return not request.user.is_authenticated


# '' => '/dashboard/'
# '' => '/accounts/login/'
def home(request):

    # AUTHENTIFICATION
    if not_auth(request):
        return redirect(settings.AUTH_URL)
    # AUTHENTIFICATION

    return redirect(settings.LOGIN_REDIRECT_URL)


# 'dashboard/'
def index(request):

    # AUTHENTIFICATION
    if not_auth(request):
        return redirect(settings.AUTH_URL)
    # AUTHENTIFICATION

    if request.user.is_authenticated:
        try:
            response = requests.get('http://127.0.0.1:5000/api/subnet')
        except ConnectionError as e:
            return render(request, 'error/Error503.html')
        json_data = response.json()
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                route = form.save(commit=False)
                requests.post('http://127.0.0.1:5000/api/subnet',
                              json={
                                  "ip": str(route.ip),
                                  "communities": str(route.community),
                                  "next_hop": str(route.next_hop)})
        else:
            form = PostForm()
        return render(request, 'route_dashboard/route_dashboard.html', {
            'data' : json_data,
            'form': form,
        })
    else:
        return redirect('/accounts/login/')


# 'accounts/change_password/'
def change_password(request):

    # AUTHENTIFICATION
    if not_auth(request):
        return redirect(settings.AUTH_URL)
    # AUTHENTIFICATION

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })
