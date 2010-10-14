from django.http import HttpResponse, \
 HttpResponseRedirect

from django.template import RequestContext
from django.shortcuts import render_to_response

from django.http import Http404
 
from models import User, User_Activation, User_Website, \
 Website, Website_Website, User_ForgetPassword

from forms import LoginForm, ChangePasswordForm, \
 SignupForm, TryitForm, ForgetPasswordForm

import sys
import re
from lib import remove_landing_url,  \
 get_http_response, get_site_description, \
 get_site_favicon_url, extract_website_name, \
 remember_user, forget_user, login_user, \
 render_form, is_logged_in, protected, public, logout_user, \
 remove_leading_http, http_read, normalize_img
 
from django.core.files.base import ContentFile
from helpers import make_random_string
  
#TODO: implement forget password, and send activation code again
#TODO: implement search

@public
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            remember_me = form.cleaned_data['remember_me']
            response = HttpResponseRedirect('/management')
            # delete autologin object and corresponding cookie of last user if exist -- safe
            forget_user(response=response, request=request)
            # after custom validation user is known to exist, and no need for password
            # since we check it in validator
            user = User.objects.get(email=email)
            ufps = user.user_forgetpassword_set.all()
            if ufps:
                ufps.delete()
                
            if remember_me:
                response = remember_user(user=user, response=response)
            
            # logged in user
            login_user(session=request.session, user=user)
            # check if the user came from somewhere and render
            return response
    # request.method is GET
    else: 
        # An unbound form
        form = LoginForm()
    return render_form('login_form.html', form, '', request)

@protected
def logout(request):
    return \
     logout_user(response=HttpResponseRedirect('/'), request=request) 

@public
def forget_password(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            response = HttpResponse("True")
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return response
            
            try:
                ufp = User_ForgetPassword.objects.get(user=user)
            except User_ForgetPassword.DoesNotExist:
                User_ForgetPassword(user=user).save()
                return response
            
            ufp.save()
            
            return response
        else:
            return HttpResponse(form._errors['email'])
    
    # for testing
    
    else:
        form = ForgetPasswordForm()
        
    return render_form('forgetpassword_form.html', form, '', request)
    
    # end testing
    raise Http404

@public
def change_password(request, token):
    try:
        ufp = User_ForgetPassword.objects.get(token=token)
    except User_ForgetPassword.DoesNotExist:
        raise Http404
    
    response = HttpResponseRedirect('/')
    
    import datetime
    now = datetime.datetime.now()
    delta = datetime.timedelta(seconds=2*60*60*24)
    expires = ufp.created_at + delta
    if now > expires:
        ufp.delete()
        return response
    
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = ufp.user
            
            ufp.delete()
            
            user.password = password
            user.save()
            
            response = HttpResponseRedirect('/management')
            
            forget_user(response=response, request=request)
            response = remember_user(user=user, response=response)
            login_user(session=request.session, user=user)
            
            return response
    else:
        form = ChangePasswordForm()
        
    return render_to_response('changepassword_form.html', {
        'form': form,
        'token': token,
    }
        ,context_instance=RequestContext(request)
    )

@public
def signup(request):
    if request.method == 'POST': 
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            fullname = form.cleaned_data['fullname']
            password = form.cleaned_data['password']
            URL = str(form.cleaned_data['URL']).lower()
            # creating the fresh user
            user = User(fullname=fullname, email=email, password=password, type=1)
            user.save()
            # creating activation record for the fresh user
            User_Activation(user=user).save()
            
            description =''
            res = get_http_response(URL)
            
            # saving website's description
            if res:
                description=get_site_description(res)[0:510]
                if len(description) >= 507:
                    description=description[0:507]+'...'
                    
            name=extract_website_name(remove_landing_url(URL))
            
            # insert the url to websites table in an unverified state 
            # associated to the fresh user -- custom validator made sure that no
            # record with same url is verified yet
            website = Website(URL=URL, name=name, description=description, type=1)
            website.save()
            
            # saving website's icon
            favicon_url = get_site_favicon_url(remove_landing_url(URL)) or ''
            if favicon_url:
                favicon_content = http_read(favicon_url) or ''
                if favicon_content:
                    favicon32 = ContentFile(normalize_img((32,32),favicon_content))
                    favicon48 = ContentFile(normalize_img((48,48),favicon_content))
                    favicon64 = ContentFile(normalize_img((64,64),favicon_content))
                    website.favicon32.save(make_random_string(32)+'-32'+'.png', favicon32)
                    website.favicon48.save(make_random_string(32)+'-48'+'.png', favicon48)
                    website.favicon64.save(make_random_string(32)+'-64'+'.png', favicon64)
            
            # the actual user-website association creation
            User_Website(user=user,website=website).save()
            response = HttpResponse('Signup successful, please activate via email')
            return response
    # request.method is GET
    else:
        form = SignupForm() # An unbound form
        
    return render_form('signup_form.html', form, '', request)

@public
def activate(request, activation_code):
    try:
        ua = User_Activation.objects.get(activation_code=activation_code)
    except User_Activation.DoesNotExist:
        raise Http404
    
    response = HttpResponseRedirect('/management')
    
    if not ua.activated_at:
        ua.activate()
        ua.save()
        
    user = ua.user
    # just in case he has a cookie
    forget_user(response=response, request=request)
    response = remember_user(user=user, response=response)
    # logged in user
    login_user(session=request.session, user=user)
    return response


# capty

import os
import subprocess
import hashlib

CAPTY = '/home/adam/Aptana Studio Workspace/AppMarx/management/capty.py'
THUMBS_DIR  = '/home/adam/Aptana Studio Workspace/AppMarx/media/screenshots/'

# screen shot service

#put them in db

def thumb(request, url):
    hash = hashlib.sha1(url).hexdigest()
    path = THUMBS_DIR + hash + '.png'

    if not os.path.isfile(path):
        try:
            subprocess.check_call([CAPTY,\
                url,\
                path])
        except subprocess.CalledProcessError:
            return HttpResponse('')

    img = open(path, 'rb').read()
    return HttpResponse(img, mimetype='image/png')

@public
def tryit(request):
    error_message = ''
    if request.method == 'POST':
        form = TryitForm(request.POST)
        if form.is_valid():
            # "normalize" the url
            URL = str(form.cleaned_data['URL']).lower()
            # test for site existence
            res = get_http_response(URL)
            if not res:
                error_message += "We can not connect '" \
                 + URL +"', Please make sure you didnt have any typos in the url field"
            # site exists
            else:
                
                # site description
                website_info = {}
                website_info['URL'] = URL
                
                # for favicon
                nolanding_url = remove_landing_url(URL)
                
                # clean url for compete
                website_info['compete_URL'] = remove_leading_http(nolanding_url)
               
                # website's name
                website_info['name'] = extract_website_name(nolanding_url)
                
                # get available description of website
                website_info['description'] = get_site_description(res)
                
                # get the website's icon
                website_info['favicon_url'] = get_site_favicon_url(nolanding_url)
                
                # for screenshot
                website_info['thumb_URL'] = nolanding_url
                
                return render_to_response('website_info.html',
                    website_info,
                    context_instance=RequestContext(request),
                )
    # request.method is GET
    else:
        form = TryitForm()
        
    return render_form('tryit_form.html', form, error_message, request)

@protected
def recommend(request, from_id, to_id):
        user_id = request.session['user_id']
        # really a server error..
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404
        try:
            from_website = Website.objects.get(id=from_id, is_verified=True)
            to_website = Website.objects.get(id=to_id, is_verified=True)
        except Website.DoesNotExist:
            raise Http404
        # make sure our user is associated with the from website
        try:
            User_Website.objects.get(user=user, website=from_website)
        except User_Website.DoesNotExist:
            raise Http404
        Website_Website(from_website=from_website, to_website=to_website).save()
        return HttpResponse('True')
