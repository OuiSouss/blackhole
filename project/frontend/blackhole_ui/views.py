"""
The ``views`` module
======================

Used to manage the various pages of the webapp
"""

import json
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.conf import settings
import requests
from requests.exceptions import ConnectionError
from route_manager.forms import PostForm
import route_manager.request_json as rq_json

requestlist = ''


def check_community(community):
    """
    Used for formating the communities

    :param community: the community to clean
    :type community: String
    :return: cleaned community
    """
    community_changed = ''
    if community in '':
        return community_changed
    for char, _ in enumerate(community):
        if((community[char] != '/') and (community[char] != '\"')
           and (community[char] != '\'') and (community[char] != '[')
           and (community[char] != ']')):
            community_changed = community_changed[:char] + community[char]
    return community_changed


def json_sort(data_json, key_col):
    """
    Used by a sorting function, regular sort (by string)

    :param data_json: data to sort
    :type data_json: json dict
    :param key_col: used for sorting
    :type data_json: json dict
    :return: specific value from json dict, the key is specified by a \
        previous function
    :return: returns 0 if the json is incorrect
    """

    try:
        return data_json[key_col]
    except KeyError:
        return 0


def json_ip_sort(data_json, key_col):
    """
    Used by a sorting function, custom sort (by ip adress)

    :param data_json: data to sort
    :type data_json: json dict
    :param key_col: used for sorting
    :type data_json: json dict
    :return: specifc value from json dict, the key is specified by a \
        previous function
    :return: returns 0 if the json is incorrect
    """

    try:
        ip_addr = data_json[key_col]
        mask = ''
        ip_no_mask = ''
        for char, _ in enumerate(ip_addr):
            if((ip_addr[char] != '/') and (mask == '')):
                ip_no_mask = ip_no_mask[:char] + ip_addr[char]
            else:
                mask = ip_addr[char]
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
                               key=lambda elem: (json_ip_sort(elem, 'ip')),
                               reverse=True)
    elif 'hop_sort' in request:
        if str(request['hop_sort']) == '1':
            json_data = sorted(json_data,
                               key=lambda elem: (
                                   json_ip_sort(elem, 'next_hop'))
                               )
        else:
            json_data = sorted(json_data,
                               key=lambda elem: (json_ip_sort(elem, 'next_hop')
                                                 ), reverse=True)
    elif 'com_sort' in request:
        community_none = list(filter(
            lambda com: com['communities'] is None, json_data))
        if community_none:
            pass
        elif str(request['com_sort']) == '1':
            json_data = sorted(json_data,
                               key=lambda elem: (
                                   json_sort(elem, 'communities'))
                               )
        else:
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'communities')
                                                 ), reverse=True)
    elif 'create_sort' in request:
        if str(request['create_sort']) == '1':
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'created_at')))
        else:
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'created_at')
                                                 ), reverse=True)
    elif 'modi_sort' in request:
        if str(request['modi_sort']) == '1':
            json_data = sorted(json_data,
                               key=lambda elem: (
                                   json_sort(elem, 'modified_at'))
                               )
        else:
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'modified_at')
                                                 ), reverse=True)
    elif 'last_sort' in request:
        if str(request['last_sort']) == '1':
            json_data = sorted(json_data,
                               key=lambda elem: (
                                   json_sort(elem, 'last_activation'))
                               )
        else:
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem,
                                                           'last_activation')
                                                 ), reverse=True)
    elif 'active_sort' in request:
        if str(request['active_sort']) == '1':
            json_data = sorted(json_data,
                               key=lambda elem: (
                                   json_sort(elem, 'is_activated'))
                               )
        else:
            json_data = sorted(json_data,
                               key=lambda elem: (json_sort(elem, 'is_activated')
                                                 ), reverse=True)
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
    global requestlist
    log_length = 500

    # AUTHENTIFICATION
    if not_auth(request):
        return redirect(settings.AUTH_URL)
    # AUTHENTIFICATION

    try:
        response = requests.get(settings.API_URL)
    except ConnectionError as exception:
        return render(request, 'error/Error503.html',
                      {'exception': exception})

    if len(requestlist) > log_length:
        requestlist = ''
    try:
        json_data = response.json()
    except ValueError as exception:
        return render(request, 'error/Error409.html',
                      {'exception': exception})
    if request.method == 'POST':
        form = PostForm(request.POST)

        json_data = sort_switcher(request.POST, json_data)
        if 'id_delete' in request.POST:
            response_actual = rq_json.delete_route(
                str(request.POST['id_delete']))
            requestlist = requestlist[:] + '| Delete ' + str(
                request.POST['id_delete']) + ': ' + str(response_actual) + ' '
            return redirect(settings.DASHBOARD_URL)
        if 'id_modify' in request.POST:
            response_actual = rq_json.put_route(
                str(request.POST['id_modify']),
                str(request.POST['ip']),
                str(request.POST['next_hop']),
                check_community(str(request.POST['communities'])))
            requestlist = requestlist[:] + '| Modify ' + str(
                request.POST['id_modify']) + ': ' + str(response_actual) + ' '
            return redirect(settings.DASHBOARD_URL)
        if 'id1' in request.POST:
            response_actual = rq_json.enable_disable_route(
                str(request.POST['id1']), False)
            requestlist = requestlist[:] + '| Disable ' + \
                str(request.POST['id1']) + ': ' + str(response_actual) + ' '
            return redirect(settings.DASHBOARD_URL)
        if 'id2' in request.POST:
            response_actual = rq_json.enable_disable_route(
                str(request.POST['id2']), True)
            requestlist = requestlist[:] + '| Enable ' + \
                str(request.POST['id2']) + ': ' + str(response_actual) + ' '
            return redirect(settings.DASHBOARD_URL)
        if 'id_to_delete' in request.POST:
            for key, values in request.POST.lists():
                if key == 'listed_id':
                    for value in values:
                        response_actual = rq_json.delete_route(
                            str(value))
                        requestlist = requestlist[:] + '| Delete ' + \
                            str(value) + ': ' + str(response_actual) + ' '
            return redirect(settings.DASHBOARD_URL)
        if 'id_to_disable' in request.POST:
            for key, values in request.POST.lists():
                if key == 'listed_id':
                    for value in values:
                        response_actual = rq_json.enable_disable_route(
                            str(value), False)
                        requestlist = requestlist[:] + '| Disable ' + \
                            str(value) + ': ' + str(response_actual) + ' '
            return redirect(settings.DASHBOARD_URL)
        if 'id_to_enable' in request.POST:
            for key, values in request.POST.lists():
                if key == 'listed_id':
                    for value in values:
                        response_actual = rq_json.enable_disable_route(
                            str(value), True)
                        requestlist = requestlist[:] + '| Enable ' + \
                            str(value) + ': ' + str(response_actual) + ' '
            return redirect(settings.DASHBOARD_URL)
        if 'export' in request.POST:
            exportfile = open(str(request.POST['export']), 'w')
            json.dump(json_data, exportfile)
            exportfile.close()
            return redirect(settings.DASHBOARD_URL)
        if 'import' in request.POST:
            try:
                importfile = open(str(request.POST['import']), 'r')
            except FileNotFoundError as exception:
                return render(request, 'error/Error404.html',
                              {'exception': exception})
            json_file = json.load(importfile)
            for to_import in json_file:
                response_actual = rq_json.post_new_route(
                    to_import['ip'],
                    to_import['next_hop'],
                    check_community(to_import['communities']))
                requestlist = requestlist[:] + \
                    '| Post:' + str(response_actual) + ' '
            return redirect(settings.DASHBOARD_URL)
        if 'command_bgp' in request.POST:
            response_actual = rq_json.post_command_bgp(
                str(request.POST['command_bgp']))
            requestlist = requestlist[:] + \
                '| ExaBGP:' + str(response_actual.text) + ' '
        if form.is_valid():
            route = form.save(commit=False)
            response_actual = rq_json.post_new_route(
                str(route.ip),
                str(route.next_hop),
                check_community(str(route.community)))
            requestlist = requestlist[:] + '| Post:' + str(response_actual)
            return redirect(settings.DASHBOARD_URL)
    else:
        form = PostForm()
    return render(request, settings.TEMPLATE_DASHBOARD, {
        'data': json_data,
        'form': form,
        'sort': request.POST,
        'response': requestlist,
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
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect(settings.CHANGE_PASSWORD)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, settings.TEMPLATE_CHANGE_PASSWORD, {
        'form': form
    })
