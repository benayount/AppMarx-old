from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response


from django import forms
from appmarx_project.users.models import User, User_Activation
from appmarx_project.websites.lib import clean_url, \
 remove_landing_url, remove_leading_http, \
 get_http_response, get_site_description, \
 get_site_favicon_img_tag, extract_website_name
 
from appmarx_project.lib import render_form

from appmarx_project.websites.forms import TryitForm

from django.http import HttpResponse, \
 HttpResponseRedirect
 
def tryit(request):
    error_message = ''
    if request.method == 'POST':
        form = TryitForm(request.POST)
        if form.is_valid():
            # "normalize" the url
            URL = remove_landing_url(str(form.cleaned_data['URL']).lower())
            # test for site existence
            #return HttpResponse(URL)
            res = get_http_response(URL)
            if not res:
                error_message += "We can not connect '" \
                 + URL +"', Please make sure you didnt have any typos in the url field"
            # site exists
            else:
                # this will be sent back to the template
                # to show the info
                website_info = {}
                website_info['URL'] = clean_url(URL)
                
                # get available description of website
                website_info['description'] = \
                 get_site_description(res)
                
                # get the website's icon
                website_info['favicon_url'] = get_site_favicon_img_tag(URL)
                
                # also pass the website's(company) name
                website_info['name'] = extract_website_name(URL)
                
                return render_to_response('website_info.html',
                    website_info,
                    context_instance=RequestContext(request),
                )
    # request.method is GET
    else:
        form = TryitForm() # An unbound form
        
    return render_form('tryit_form.html', form, error_message, request)

