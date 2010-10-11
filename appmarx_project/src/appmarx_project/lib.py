from django.template import RequestContext
from django.shortcuts import render_to_response

import libxml2dom
import urllib2

from urllib2 import URLError, HTTPError

import random
import string


# self explanatory

def make_random_string(length):
    return "".join(random.sample(string.letters+string.digits, length))

def render_form(template, form, error_message, request):
    return render_to_response(template, {
        'form': form,
        'error_message': error_message,
    }
        ,context_instance=RequestContext(request) # -- will load request object into template
    )
    
def get_http_response(url):
    req = urllib2.Request(url)
    try:
        res = urllib2.urlopen(req)
    except (URLError, HTTPError):
        return False
    return res

# access dict values safely(no exception)

def safe_dict_get(dict, key):
    try:
        value = dict[key]
    except KeyError:
        return None
    return value

# @save_lastvisited decorator -- saves last visited path in session
# after view execution

def save_lastvisited(view):
    def save_lastvisited_wrapper(request):
        response = view(request)
        request.session['last_visited_path'] = request.path
        return response
    return save_lastvisited_wrapper

        