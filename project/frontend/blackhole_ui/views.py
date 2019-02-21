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
    """
    Used by a sorting function, regular sort (by string)

    :param request: json dict
    :return: specifc value from json dict, the key is specified by a previous function
    :return: returns 0 if the json is incorrect
    """
    global global_column
    try:
        return json[global_column]
    except KeyError:
        return 0


def json_ip_sort(json):
    """
    Used by a sorting function, custom sort (by ip adress)

    :param request: json dict
    :return: specifc value from json dict, the key is specified by a previous function
    :return: returns 0 if the json is incorrect
    """
    global global_column
    try:
        ip = json[global_column]
        return tuple(int(part) for part in ip.split('.'))
    except KeyError:
        return 0



def sort_by(json, key_col):
    """
    Sorting function, regular sort (by string)


    ### Why we can't do it in one line

    Sorting in one line with lambda expression is not possible
    because there may be 'KeyError' exceptions when reading json.
    Therefore another sub function must be used to handle exceptions.


    ### Why we prefer not duplicate code

    It is not necessary to create a sub function for each 'column'
    to sort because the sorting method is the same. That would
    needlessly duplicate code as only the name of the 'key' would change.


    ### Sorting function constraints

    Sorting functions cannot handle additionnal arguments.
    Only the data and the function to sort are processed.


    ### How we handle constraints

    Therefore the 'column key' is specified via a global variable,
    that will be used immediately and only by the sub sorting function.


    :param json: list of routes (json format)
    :param key_col: key of the column to sort
    :return: sorted list of routes by a specified column
    """
    global global_column
    global_column = key_col
    return sorted(json, key=json_sort)



def sort_by_ip(json, key_col):
    """
    Sorting function, custom sort (by ip adress)


    ### Why we can't do it in one line

    Sorting in one line with lambda expression is not possible
    because there may be 'KeyError' exceptions when reading json.
    Therefore another sub function must be used to handle exceptions.


    ### Why we prefer not duplicate code

    It is not necessary to create a sub function for each 'column'
    to sort because the sorting method is the same. That would
    needlessly duplicate code as only the name of the 'key' would change.


    ### Sorting function constraints

    Sorting functions cannot handle additionnal arguments.
    Only the data and the function to sort are processed.


    ### How we handle constraints

    Therefore the 'column key' is specified via a global variable,
    that will be used immediately and only by the sub sorting function.


    :param json: list of routes (json format)
    :param key_col: key of the column to sort
    :return: sorted list of routes by a specified column
    """
    global global_column
    global_column = key_col
    return sorted(json, key=json_ip_sort)

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
        json_data = sort_by_ip(json_data, 'ip')
    elif 'hop_sort' in request:
        json_data = sort_by_ip(json_data, 'next_hop')
    elif 'com_sort' in request:
        json_data = sort_by(json_data, 'communities')
    elif 'create_sort' in request:
        json_data = sort_by(json_data, 'created_at')
    elif 'modi_sort' in request:
        json_data = sort_by(json_data, 'modified_at')
    elif 'last_sort' in request:
        json_data = sort_by(json_data, 'last_activation')
    elif 'active_sort' in request:
        json_data = sort_by(json_data, 'is_activated')
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
        else:
            json_data = sort_switcher(request.POST, json_data)
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
