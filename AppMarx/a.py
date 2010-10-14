import Image
import urllib2
import sys
from django.core.files.base import ContentFile
import ImageFile


im=Image.open('/home/adam/Aptana Studio Workspace/AppMarx/favicon.ico')
border=Image.open('/home/adam/Aptana Studio Workspace/AppMarx/media/lib/bordered_transparent.png')
border.paste(im, (10,10))

import ImageFont, ImageDraw

draw = ImageDraw.Draw(border)
font = ImageFont.truetype("arial.ttf", 9)
draw.text((4, 22), "hello", font=font, fill='rgb(0,0,0)')

border.save("/home/adam/Aptana Studio Workspace/AppMarx/sasas1.png", "png")

