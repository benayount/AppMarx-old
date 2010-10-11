from django.template import Context, loader, RequestContext
from django.http import HttpResponse, \
 HttpResponseRedirect
 
from django.http import Http404
 
from django.shortcuts import render_to_response

from django import forms
from appmarx_project.users.models import User, User_Activation, User_Website
from appmarx_project.websites.lib import clean_url, get_site_description, \
 remove_landing_url, extract_website_name

from appmarx_project.websites.models import Website

from appmarx_project.users.lib import authenticate_user, remember_user, forget_user, \
 check_autologin, login_user
 
from appmarx_project.lib import render_form, safe_dict_get

from appmarx_project.users.forms import LoginForm, \
 SignupForm
 
from datetime import datetime, timedelta
import datetime

from appmarx_project.defines import *

#TODO: add autologin and save last visited url before each request and write autologin()
@check_autologin
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            remember_me = form.cleaned_data['remember_me']
            response = HttpResponseRedirect('/')
            # delete autologin object and corresponding cookie of last user if exist -- safe
            forget_user(response=response, request=request)
            # after custom validation user is known to exist, and no need for password
            # since we check it in validator
            user = User.objects.get(email=email)
            if remember_me:
                response = remember_user(user=user, response=response)
            
            # logged in user
            login_user(session=request.session, user=user)
            return response
    # request.method is GET
    else: 
        # An unbound form
        form = LoginForm()
    return render_form('login_form.html', form, '', request)
    
def signup(request):
    if request.method == 'POST': 
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            fullname = form.cleaned_data['fullname']
            password = form.cleaned_data['password']
            URL = remove_landing_url(str(form.cleaned_data['URL']).lower())
            # creating the fresh user
            user = User(fullname=fullname, email=email, password=password, type=1)
            user.save()
            # creating activation record for the fresh user
            User_Activation(user=user).save()
            # insert the url to websites table in an unverified state 
            # associated to the fresh user -- custom validator made sure that no
            # record with same url is verified yet
            website = Website(URL=URL, name=extract_website_name(URL), type=1)
            website.save()
            # the actual user-website association creation
            User_Website(user=user,website=website).save()
            response = HttpResponseRedirect('/')
            forget_user(response=response, request=request)
            user = User.objects.get(email=email)
            response = remember_user(user=user, response=response)
            # logged in user
            login_user(session=request.session, user=user)
            # logged in
            return response
    # request.method is GET
    else:
        form = SignupForm() # An unbound form
        
    return render_form('signup_form.html', form, '', request)

def activate(request, activation_code):
    try:
        ua = User_Activation.objects.get(activation_code=activation_code)
    except User_Activation.DoesNotExist:
        raise Http404
    
    if ua.activated_at:
        return HttpResponse('Your account already been activated')
    
    ua.activate()
    ua.save()
    user = ua.user
    response = HttpResponse('Your account has been activated.')
    # just in case he has a cookie
    forget_user(response=response, request=request)
    response = remember_user(user=user, response=response)
    # logged in user
    login_user(session=request.session, user=user)
    return response