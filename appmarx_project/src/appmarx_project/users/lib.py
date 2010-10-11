from django.core.exceptions import *
from appmarx_project.users.models import User, User_AutoLogin
from appmarx_project.lib import safe_dict_get
from django.conf import settings
from datetime import datetime, timedelta
import datetime
import sys
import hashlib

def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    if user.encrypted_password != hashlib.sha1(user.salt+password).hexdigest():
        return None
    return user

def remember_user(user, response):
    max_age = 60*60*24*14 # 2 weeks
    # format time to mysql datetime format
    expires = datetime.datetime.strftime(datetime.datetime.now() \
     + datetime.timedelta(seconds=max_age), "%Y-%m-%d %H:%M:%S")
    ua = User_AutoLogin(user=user, expires_at=expires)
    ua.save()
    response.set_cookie('auth_token', value={'user_id' : user.id, 'remember_token' : ua.remember_token} , \
     max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN or None, \
     secure=settings.SESSION_COOKIE_SECURE or None)
    return response

def forget_user(response, request):
    auth_token = safe_dict_get(request.COOKIES, 'auth_token')
    if auth_token:
        try:
            # cookies are strings, need to eval them, but they might be invalid
            try:
                auth_token = eval(auth_token)
            except Exception:
                return
            user = User.objects.get(id=safe_dict_get(auth_token, 'user_id'))
            ua = User_AutoLogin.objects.get(user=user, remember_token=safe_dict_get(auth_token, 'remember_token'))
            # delete auto login record from db
            ua.delete()
        except (User.DoesNotExist, User_AutoLogin.DoesNotExist):
            pass
        # delete corresponding cookie
        response.delete_cookie('auth_token', domain=settings.SESSION_COOKIE_DOMAIN or None)
        
def autologin(request):
    # if user logged in, no need to check auto login
    if safe_dict_get(request.session, 'user_id'):
        return
     
    auth_token = safe_dict_get(request.COOKIES, 'auth_token')
    if auth_token:
        try:
            auth_token = eval(auth_token)
        except Exception:
            return
        try:
            user = User.objects.get(id=safe_dict_get(auth_token, 'user_id'))
            ua = User_AutoLogin.objects.get(user=user, remember_token=safe_dict_get(auth_token, 'remember_token'))
        except (User.DoesNotExist, User_AutoLogin.DoesNotExist):
            return
        # check if cookie expired and delete db record
        now = datetime.datetime.now()
        expires = ua.expires_at
        if now > expires:
            ua.delete()
            return
        
        # log in user
        request.session['user_id'] = user.id
        request.session['user'] = user


# check_autologin decorator
# put @check_autologin above a view, to check autologin before its exec

def check_autologin(view):
    def autologin_wrapper(request):
        autologin(request)
        return view(request)
    return autologin_wrapper

# just assigning the user to session

def login_user(session, user):
    session['user_id'] = user.id
    session['user'] = user