import Image
import urllib2
import sys
from django.core.files.base import ContentFile
import ImageFile


im=Image.open('/home/adam/Aptana Studio Workspace/AppMarx/favicon.ico')
border=Image.open('/home/adam/Aptana Studio Workspace/AppMarx/media/lib/bordered_transparent.png')
border.paste(im, (10,10))
border.save("/home/adam/Aptana Studio Workspace/AppMarx/media/tmp/sasas1.png", "png")

