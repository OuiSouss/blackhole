from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.conf import settings
import requests
from requests.exceptions import ConnectionError
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

    return redirect(settings.DASHBOARD_URL)


# 'dashboard/'
def index(request):

    # AUTHENTIFICATION
    if not_auth(request):
        return redirect(settings.AUTH_URL)
    # AUTHENTIFICATION


    try:
        response = requests.get(settings.API_URL)
    except ConnectionError as exception:
        return render(request, 'error/Error503.html',
                      {'exception' : exception})
    json_data = response.json()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            requests.post(settings.API_URL,
                          json={
                              "ip": str(route.ip),
                              "communities": str(route.community),
                              "next_hop": str(route.next_hop)})
        else:
            print(request.POST)
            if 'id' in request.POST:
                requests.delete(settings.API_URL,
                                json={"id": str(request.POST['id'])})
            else:
                if 'id1' in request.POST:
                    requests.patch(settings.API_URL,
                                   json={
                                       "id": str(request.POST['id1']),
                                       "is_activated": False })
                else:
                    if 'id2' in request.POST:
                        requests.patch(settings.API_URL,
                                       json={
                                           "id": str(request.POST['id2']),
                                           "is_activated": True})
        return redirect(settings.DASHBOARD_URL)
    else:
        form = PostForm()
    return render(request, settings.TEMPLATE_DASHBOARD, {
        'data' : json_data,
        'form': form,
    })



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
            return redirect(settings.CHANGE_PASSWORD)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, settings.TEMPLATE_CHANGE_PASSWORD, {
        'form': form
    })
