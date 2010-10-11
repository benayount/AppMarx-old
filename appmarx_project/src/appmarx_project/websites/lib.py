import re
from urllib2 import URLError, HTTPError
import urllib2
import simplejson
import libxml2dom

from appmarx_project.lib import get_http_response
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

def clean_url(url):
    return remove_landing_url(remove_leading_http(url))

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

    
    
def get_site_favicon_img_tag(url):
    # twitter trial for favicon
    default_images_sizes = [2483, 1073, 1233, 1381]
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
    