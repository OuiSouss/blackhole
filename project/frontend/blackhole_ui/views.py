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
import json

def check_community(community):
    community_changed = ''
    for a in range(len(community)):
            if((community[a] != '/') and (community[a] != '\"') and (community[a] != '\'') and (community[a] != '[') and (community[a] != ']')):
                community_changed = community_changed[:a] + community[a]
    return community_changed

def json_sort(json, key_col):
    """
    Used by a sorting function, regular sort (by string)

    :param request: json dict
    :return: specifc value from json dict, the key is specified by a \
        previous function
    :return: returns 0 if the json is incorrect
    """

    try:
        return json[key_col]
    except KeyError:
        return 0

def json_ip_sort(json, key_col):
    """
    Used by a sorting function, custom sort (by ip adress)

    :param request: json dict
    :return: specifc value from json dict, the key is specified by a \
        previous function
    :return: returns 0 if the json is incorrect
    """

    try:
        ip = json[key_col]
        mask = ''
        ip_no_mask = ''
        for a in range(len(ip)):
            if((ip[a] != '/') and (mask == '')):
                ip_no_mask = ip_no_mask[:a] + ip[a]
            else:
                mask = ip[a]
        return tuple(int(part) for part in ip_no_mask.split('.'))
    except KeyError:
        return 0

def sort_switcher(request, json_data):
    """
    sort_switcher implement a switcher to sort what we want


    :param request: request.POST
    :type request: dict
    :param json_data: response in json format
    :type json_data: dict
    :return: json_data
    :rtype: dict
    """
    if 'net_sort' in request:
        if str(request['net_sort']) == '1':
            json_data = sorted(json_data,
                               key=lambda elem: (json_ip_sort(elem, 'ip')))
        else:
            json_data = sorted(json_data,
                               key=lambda elem: (json_ip_sort(elem, 'ip')), reverse=True)
    elif 'hop_sort' in request:
        if str(request['hop_sort']) == '1':
            json_data = sorted(json_data,
                               key=lambda elem: (json_ip_sort(elem, 'next_hop')))
        else:
            json_data = sorted(json_data,
                               key=lambda elem: (json_ip_sort(elem, 'next_hop')), reverse=True)
    elif 'com_sort' in request:
        if str(request['com_sort']) == '1':
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'communities')))
        else:
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'communities')), reverse=True)
    elif 'create_sort' in request:
        if str(request['create_sort']) == '1':
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'created_at')))
        else:
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'created_at')), reverse=True)
    elif 'modi_sort' in request:
        if str(request['modi_sort']) == '1':
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'modified_at')))
        else:
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'modified_at')), reverse=True)
    elif 'last_sort' in request:
        if str(request['last_sort']) == '1':
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'last_activation')))
        else:
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'last_activation')), reverse=True)
    elif 'active_sort' in request:
        if str(request['active_sort']) == '1':
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'is_activated')))
        else:
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'is_activated')), reverse=True)
    return json_data

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

        json_data = sort_switcher(request.POST, json_data)
        if 'id_delete' in request.POST:
            route_manager.request_json.delete_route(
                str(request.POST['id_delete']))
            return redirect(settings.DASHBOARD_URL)
        if 'id_modify' in request.POST:
            route_manager.request_json.put_route(
                str(request.POST['id_modify']),
                str(request.POST['ip']),
                str(request.POST['next_hop']),
                check_community(str(request.POST['communities'])))
            return redirect(settings.DASHBOARD_URL)
        if 'id1' in request.POST:
            route_manager.request_json.enable_disable_route(
                str(request.POST['id1']), False)
            return redirect(settings.DASHBOARD_URL)
        if 'id2' in request.POST:
            route_manager.request_json.enable_disable_route(
                str(request.POST['id2']), True)
            return redirect(settings.DASHBOARD_URL)
        if 'id_to_delete' in request.POST:
            for key, values in request.POST.lists():
                if key=='listed_id':
                    for value in values:
                        route_manager.request_json.delete_route(
                            str(value))
            return redirect(settings.DASHBOARD_URL)
        if 'id_to_disable' in request.POST:
            for key, values in request.POST.lists():
                if key=='listed_id':
                    for value in values:
                        route_manager.request_json.enable_disable_route(
                            str(value), False)
            return redirect(settings.DASHBOARD_URL)
        if 'id_to_enable' in request.POST:
            for key, values in request.POST.lists():
                if key=='listed_id':
                    for value in values:
                        route_manager.request_json.enable_disable_route(
                            str(value), True)
            return redirect(settings.DASHBOARD_URL)
        if 'export' in request.POST:
            exportfile=open('data.json', 'w')
            json.dump(json_data, exportfile)
            exportfile.close()
            return redirect(settings.DASHBOARD_URL)
    else:
        form = PostForm()
    return render(request, settings.TEMPLATE_DASHBOARD, {
        'data' : json_data,
        'form': form,
        'sort' : request.POST,
        'response' : response,
        'request' : request,
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
