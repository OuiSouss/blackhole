"""
The ``views`` module
======================

Used to manage the various pages of the webapp
"""

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.conf import settings
import requests
from requests.exceptions import ConnectionError
from route_manager.forms import PostForm
import route_manager.request_json

global_column = None

def json_sort(json):
    global global_column
    try:
        return json[global_column]
    except KeyError:
        return 0

def sort_by(json, key_col):
    global global_column
    global_column = key_col
    return sorted(json, key=json_sort)

def not_auth(request):
    """
    Checks if the user is currently anonymous

    :param request: the request page
    :return: True for anonymous, False for authenticated
    """
    return not request.user.is_authenticated

def home(request):
    """
    Activated when trying to access the root page (/)

    :param request: the request page
    :return: dashboard for authenticated, login page for anonymous
    """

    # AUTHENTIFICATION
    if not_auth(request):
        return redirect(settings.AUTH_URL)
    # AUTHENTIFICATION

    return redirect(settings.DASHBOARD_URL)

def index(request):
    """
    Activated when trying to access the dashboard

    The entire dashboard will update for each modification.
    It would have been preferable to update only the concerned elements,
    but that would require javascript and more development time.

    :param request: the request page
    :return: dashboard for authenticated, login page for anonymous
    """

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
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            route_manager.request_json.post_new_route(route)
            return redirect(settings.DASHBOARD_URL)
        else:
            if 'net_sort' in request.POST:
                json_data = sort_by(json_data, 'ip')
            elif 'hop_sort' in request.POST:
                json_data = sort_by(json_data, 'next_hop')
            elif 'com_sort' in request.POST:
                json_data = sort_by(json_data, 'communities')
            elif 'create_sort' in request.POST:
                json_data = sort_by(json_data, 'created_at')
            elif 'modi_sort' in request.POST:
                json_data = sort_by(json_data, 'modified_at')
            elif 'last_sort' in request.POST:
                json_data = sort_by(json_data, 'last_activation')
            elif 'active_sort' in request.POST:
                json_data = sort_by(json_data, 'is_activated')
            if 'id_delete' in request.POST:
                route_manager.request_json.delete_route(
                    str(request.POST['id_delete']))
                return redirect(settings.DASHBOARD_URL)
            else:
                if 'id_modify' in request.POST:
                    route_manager.request_json.put_route(
                        str(request.POST['id_modify']),
                        str(request.POST['ip']),
                        str(request.POST['next_hop']),
                        str(request.POST['communities']))
                    return redirect(settings.DASHBOARD_URL)
                else:
                    if 'id1' in request.POST:
                        route_manager.request_json.enable_disable_route(
                            str(request.POST['id1']), False)
                        return redirect(settings.DASHBOARD_URL)
                    else:
                        if 'id2' in request.POST:
                            route_manager.request_json.enable_disable_route(
                                str(request.POST['id2']), True)
                            return redirect(settings.DASHBOARD_URL)
    else:
        form = PostForm()
    return render(request, settings.TEMPLATE_DASHBOARD, {
        'data' : json_data,
        'form': form,
    })

def change_password(request):
    """
    Activated when trying to access the change_password page

    :param request: the request page
    :return: change_password page for authenticated, login page for anonymous
    """

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
