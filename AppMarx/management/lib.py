import re
import simplejson
import libxml2dom
import datetime
import hashlib
import sys
import os
import subprocess

from django.conf import settings

from defines import *
from django.core.exceptions import *
from models import User, User_AutoLogin

from django.template import RequestContext
from django.shortcuts import render_to_response
import urllib2
from urllib2 import URLError, HTTPError
from django.http import HttpResponseRedirect

from helpers import safe_dict_get, make_random_string
# check if a user logged in

def is_logged_in(request):
    if safe_dict_get(request.session, 'user_id'):
        return True
    return False
   

# strips leading http[s]?:// and trailing /.*
# clean_url('http://www.appmarx.com/users/tryit') ==
# www.appmarx.com

def remove_leading_http(url):
    return re.sub('^http[s]?:\/\/', '', url)

def remove_landing_url(url):
    prefix = ''
    prefix_match = re.match('^http[s]?:\/\/', url)
    if prefix_match is not None:
        prefix = url[prefix_match.start():prefix_match.end()]
        url = re.sub('^http[s]?:\/\/', '', url)
    url = re.sub('\/.*', '', url)
    return prefix+url

def get_site_description(res):
    doc = libxml2dom.parseString(res.read(), html=1)
    meta_tag_nodes = doc.getElementsByTagName('meta')
    
    for meta_tag_node in meta_tag_nodes:
        if str(meta_tag_node.getAttribute('name')).lower() == "description":
            return meta_tag_node.getAttribute('content')
    
    # if description meta was not found, try google
    url = ('http://ajax.googleapis.com/ajax/services/search/web' \
           '?v=1.0&q=site:'+res.url)
    res = get_http_response(url)
    results = simplejson.load(res)['responseData']['results']
    if results:
        return results[0]['content']
    return 'No description available'

def extract_website_name(url):
    url = remove_leading_http(url)
    url_suffixes = \
    [ \
    'AD', \
    'AE', \
    'AF', \
    'AG', \
    'AI', \
    'AL', \
    'AM', \
    'AN', \
    'AO', \
    'AQ', \
    'AR', \
    'AS', \
    'AT', \
    'AU', \
    'AW', \
    'AX', \
    'AZ', \
    'BA', \
    'BB', \
    'BD', \
    'BE', \
    'BF', \
    'BG', \
    'BH', \
    'BI', \
    'BJ', \
    'BM', \
    'BN', \
    'BO', \
    'BR', \
    'BS', \
    'BT', \
    'BV', \
    'BW', \
    'BY', \
    'BZ', \
    'CA', \
    'CC', \
    'CD', \
    'CF', \
    'CG', \
    'CH', \
    'CI', \
    'CK', \
    'CL', \
    'CM', \
    'CN', \
    'CO', \
    'CO.IL', \
    'CR', \
    'CS', \
    'CU', \
    'CV', \
    'CX', \
    'CY', \
    'CZ', \
    'DE', \
    'DJ', \
    'DK', \
    'DM', \
    'DO', \
    'DZ', \
    'EC', \
    'EE', \
    'EG', \
    'EH', \
    'ER', \
    'ES', \
    'ET', \
    'FI', \
    'FJ', \
    'FK', \
    'FM', \
    'FO', \
    'FR', \
    'FX', \
    'GA', \
    'GB', \
    'GD', \
    'GE', \
    'GF', \
    'GH', \
    'GI', \
    'GL', \
    'GM', \
    'GN', \
    'GP', \
    'GQ', \
    'GR', \
    'GS', \
    'GT', \
    'GU', \
    'GW', \
    'GY', \
    'HK', \
    'HM', \
    'HN', \
    'HR', \
    'HT', \
    'HU', \
    'ID', \
    'IE', \
    'IL', \
    'IN', \
    'IO', \
    'IQ', \
    'IR', \
    'IS', \
    'IT', \
    'JM', \
    'JO', \
    'JP', \
    'KE', \
    'KG', \
    'KH', \
    'KI', \
    'KM', \
    'KN', \
    'KP', \
    'KR', \
    'KW', \
    'KY', \
    'KZ', \
    'LA', \
    'LB', \
    'LC', \
    'LI', \
    'LK', \
    'LR', \
    'LS', \
    'LT', \
    'LU', \
    'LV', \
    'LY', \
    'MA', \
    'MC', \
    'MD', \
    'MG', \
    'MH', \
    'MK', \
    'ML', \
    'MM', \
    'MN', \
    'MO', \
    'MP', \
    'MQ', \
    'MR', \
    'MS', \
    'MT', \
    'MU', \
    'MV', \
    'MW', \
    'MX', \
    'MY', \
    'MZ', \
    'NA', \
    'NC', \
    'NE', \
    'NF', \
    'NG', \
    'NI', \
    'NL', \
    'NO', \
    'NP', \
    'NR', \
    'NU', \
    'NZ', \
    'OM', \
    'PA', \
    'PE', \
    'PF', \
    'PG', \
    'PH', \
    'PK', \
    'PL', \
    'PM', \
    'PN', \
    'PR', \
    'PS', \
    'PT', \
    'PW', \
    'PY', \
    'QA', \
    'RE', \
    'RO', \
    'RU', \
    'RW', \
    'SA', \
    'SB', \
    'SC', \
    'SD', \
    'SE', \
    'SG', \
    'SH', \
    'SI', \
    'SJ', \
    'SK', \
    'SL', \
    'SM', \
    'SN', \
    'SO', \
    'SR', \
    'ST', \
    'SU', \
    'SV', \
    'SY', \
    'SZ', \
    'TC', \
    'TD', \
    'TF', \
    'TG', \
    'TH', \
    'TJ', \
    'TK', \
    'TL', \
    'TM', \
    'TN', \
    'TO', \
    'TP', \
    'TR', \
    'TT', \
    'TV', \
    'TW', \
    'TZ', \
    'UA', \
    'UG', \
    'UK', \
    'UM', \
    'US', \
    'UY', \
    'UZ', \
    'VA', \
    'VC', \
    'VE', \
    'VG', \
    'VI', \
    'VN', \
    'VU', \
    'WF', \
    'WS', \
    'YE', \
    'YT', \
    'YU', \
    'ZA', \
    'ZM', \
    'ZR', \
    'ZW', \
    'BIZ', \
    'COM', \
    'EDU', \
    'GOV', \
    'INT', \
    'MIL', \
    'NET', \
    'ORG', \
    'PRO', \
    'AERO', \
    'ARPA', \
    'COOP', \
    'INFO', \
    'NAME', \
    'NATO', \
    ]
    for suffix in url_suffixes:
        p = re.search('\.'+suffix+'$', url, flags=re.IGNORECASE)
        if p is not None:
            url = url[0:p.start()]
            p = re.search('\.[a-zA-Z0-9-]+$', url)
            if p is None:
                return url
            return url[(p.start()+1):p.end()+1]
    return ''

def get_site_favicon_url(url):
    # twitter trial for favicon
    default_images_sizes = [2483, 1073, 1233, 1381, 1402]
    website_name = extract_website_name(url)
    image_url = 'http://img.tweetimag.es/i/'+website_name
    res = get_http_response(image_url)
    if res is not None:
        image_size = len(res.read())
        is_default_image = False
        for default_image_size in default_images_sizes:
            if default_image_size == image_size:
                is_default_image = True
        if not is_default_image:
            return image_url
    
    # get favicon
    image_url = url+'/favicon.ico'
    res = get_http_response(image_url)
    if res is not None:
        return image_url
    
    return None

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
    # set the cookie
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
    return response

# just assigning the user to session

def login_user(session, user):
    session['user_id'] = user.id
    session['user'] = user
    
def logout_user(response, request):
    response = forget_user(response=response, request=request)
    del request.session['user_id']
    del request.session['user']
    return response

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
        return None
    return res
     
def autologin(request):
    # if user logged in, no need to check auto login
    if safe_dict_get(request.session, 'user_id'):
        return request
     
    auth_token = safe_dict_get(request.COOKIES, 'auth_token')
    if auth_token:
        try:
            auth_token = eval(auth_token)
        except Exception:
            return request
        try:
            user = User.objects.get(id=safe_dict_get(auth_token, 'user_id'))
            ua = User_AutoLogin.objects.get(user=user, remember_token=safe_dict_get(auth_token, 'remember_token'))
        except (User.DoesNotExist, User_AutoLogin.DoesNotExist):
            return request
        # check if cookie expired and delete db record
        now = datetime.datetime.now()
        expires = ua.expires_at
        if now > expires:
            ua.delete()
            return request
        
        # log in user
        request.session['user_id'] = user.id
        request.session['user'] = user
    return request


# try to auto login and save last visited url

def session_maintenance(request):
    request = autologin(request)
    return request

# protected views decorator
# will redirect to root if not logged in
def protected(view):
    def wrapper(request, *args, **kwargs):
        request = session_maintenance(request)
        if not is_logged_in(request):
            return HttpResponseRedirect('/')
        return view(request, *args, **kwargs)
    return wrapper

# public views decorator
# will redirect to /management if logged in
def public(view):
    def wrapper(request, *args, **kwargs):
        request = session_maintenance(request)
        if is_logged_in(request):
            return HttpResponseRedirect('/management')
        return view(request, *args, **kwargs)
    return wrapper

def http_read(url):
    res = get_http_response(url)
    if res:
        return res.read()
    return None

def normalize_img((width, height), data):
    import ImageFile
    import Image
    p = ImageFile.Parser()
    p.feed(data)
    im=p.close()
    # small images processing(framing etc..)
    if im.size[0]<=22 and im.size[1]<=22:
        # normalize the small image
        #im = im.resize((16,16), Image.ANTIALIAS)
        
        # create our temp file names (to be removed soon)
        tmp_filename=[]
        for i in range(0,5):
            tmp_filename.append(settings.TMP_IMAGES_FOLDER+make_random_string(length=32)+'.png')
        
        im.save(tmp_filename[0],'png')
        
        # using ImageMagick
        try:
            subprocess.call(['convert','-bordercolor', 'none', '-border', '10', '-mattecolor', 'none','-frame', '2x2',tmp_filename[0],tmp_filename[1]])
            subprocess.call(['convert',tmp_filename[1],'-border','3','-alpha', 'transparent','-background', 'none','-fill','white','-stroke','none','-strokewidth','0','-draw','@'+settings.IMAGES_LIB_FOLDER+'rounded_corner.mvg',tmp_filename[2]])
            subprocess.call(['convert',tmp_filename[1],'-border', '3', '-alpha','transparent','-background','none','-fill', 'none', '-stroke', '#CCC', '-strokewidth', '3', '-draw' ,'@'+settings.IMAGES_LIB_FOLDER+'rounded_corner.mvg', tmp_filename[3]])
            subprocess.call(['convert',tmp_filename[1],'-matte','-bordercolor', 'none', '-border', '3',tmp_filename[2],'-compose', 'DstIn', '-composite',tmp_filename[3],'-compose', 'Over','-composite', tmp_filename[4]])
        except (subprocess.CalledProcessError,OSError):
            return ''
        
        im = Image.open(tmp_filename[4])
        
        # removal of tmp files
        
        for i in range(0,5):
            os.remove(tmp_filename[i])
        
    im = im.resize((width,height), Image.ANTIALIAS)
    tmp_filename = make_random_string(length=32)
    tmp_file_full_path = settings.TMP_IMAGES_FOLDER+tmp_filename+'.png'
    im.save(tmp_file_full_path, 'png')
    tmp_file = open(tmp_file_full_path,'r')
    tmp_file_content = tmp_file.read()
    os.remove(tmp_file_full_path)
    return tmp_file_content

# capty

def tryit_screenshot(url):
    hash = hashlib.sha1(url).hexdigest()
    path = settings.SCREENSHOTS_FOLDER + hash + '.png'

    if not os.path.isfile(path):
        try:
            subprocess.check_call([settings.CAPTY,\
                url,\
                path])
        except subprocess.CalledProcessError:
            return None
        
        return settings.MEDIA_URL+'screenshots/'+ hash + '.png'
    
def site_screenshot(url):
    random_string = make_random_string(32)
    path = settings.TMP_IMAGES_FOLDER + random_string + '.png'
    try:
        subprocess.check_call([settings.CAPTY,\
            url,\
            path])
    except subprocess.CalledProcessError:
        return None
    data = open(path,'rd').read()
    os.remove(path)
    return data