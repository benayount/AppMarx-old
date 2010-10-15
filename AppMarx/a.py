import Image
import urllib2
import sys
from django.core.files.base import ContentFile
import ImageFile
import subprocess

"""
import ImageFont, ImageDraw

draw = ImageDraw.Draw(border)
font = ImageFont.truetype("arial.ttf", 9)
draw.text((4, 22), "hello1", font=font, fill='rgb(0,0,0)')

border.save("/home/adam/Aptana Studio Workspace/AppMarx/sasas1.png", "png")composite -compose Over -quality 100 -gravity NorthWest cornermask_upper_left.png favicon.png favicon.pngnw

composite -compose Over -quality 100 -gravity NorthWest cornermask_upper_left.png favicon1.png favicon1nw
composite -compose Over -quality 100 -gravity SouthWest cornermask_lower_left.png favicon1nw favicon1sw
composite -compose Over -quality 100 -gravity NorthEast cornermask_upper_right.png favicon1sw favicon1ne
composite -compose Over -quality 100 -gravity SouthEast cornermask_lower_right.png favicon1ne favicon1mask
convert favicon1mask -transparent "#ff00f6" favicon1.png

composite -compose Over -quality 100 -gravity NorthWest cornermask_upper_left.png favicon.png favicon.pngnw
composite -compose Over -quality 100 -gravity SouthWest cornermask_upper_left.png favicon1.png favicon1.pngsw
composite -compose Over -quality 100 -gravity NorthEast cornermask_upper_left.png favicon1.png favicon1.pngne
composite -compose Over -quality 100 -gravity SouthEast cornermask_upper_left.png favicon1.png favicon1.pngse
convert favicon1.pngmask -transparent "#ff00f6" favicon1.png

"""
import random
import string
import os

# self explanatory

def make_random_string(length):
    return "".join(random.sample(string.letters+string.digits, length))

TMP_IMAGES_FOLDER = "media/tmp/"

tmp_filename=[]
for i in range(0,5):
    tmp_filename.append(TMP_IMAGES_FOLDER+make_random_string(length=32)+'.png')
tmp_mvg = TMP_IMAGES_FOLDER+make_random_string(length=32)+'.mvg'

print 'convert -bordercolor none -border 10 -mattecolor none -frame 2x2 favicon.png '+tmp_filename[1]+' && convert '+tmp_filename[1]+' -format \"roundrectangle 1,1 %[fx:w+4],%[fx:h+4] 5,5\" info: > '+tmp_mvg

subprocess.call(["convert","-bordercolor","none","-border","10","-mattecolor" ,"none" ,"-frame","2x2","favicon.png","a.png"])
"""+' && convert '+tmp_filename[1]+' -format \"roundrectangle 1,1 %[fx:w+4],%[fx:h+4] 5,5\" info: > '+tmp_mvg+' && convert '+tmp_filename[1]+' -border 3 -alpha transparent -background none -fill white -stroke none -strokewidth 0 -draw \"@'+tmp_mvg+'\" '+tmp_filename[2]+' && convert '+tmp_filename[1]+' -border 3 -alpha transparent -background none -fill none -stroke \"#CCC\" -strokewidth 3 -draw \"@'+tmp_mvg+'\" '+tmp_filename[3]+' && convert '+tmp_filename[1]+' -matte -bordercolor none -border 3 '+tmp_filename[2]+' -compose DstIn -composite '+tmp_filename[3]+' -compose Over -composite '+tmp_filename[4])"""

#im = Image.open(tmp_filename[4])


"""
'+tmp_filename[0]+'
convert -bordercolor none -border 10 -mattecolor none -frame 2x2 favicon.png favicon1.png && convert favicon1.png -format 'roundrectangle 1,1 %[fx:w+4],%[fx:h+4] 5,5' info: > rounded_corner.mvg && convert favicon1.png -border 3 -alpha transparent -background none -fill white -stroke none -strokewidth 0 -draw "@rounded_corner.mvg" rounded_corner_mask.png && convert favicon1.png -border 3 -alpha transparent -background none -fill none -stroke "#CCC" -strokewidth 3 -draw "@rounded_corner.mvg" rounded_corner_overlay.png && convert favicon1.png -matte -bordercolor none -border 3 rounded_corner_mask.png -compose DstIn -composite rounded_corner_overlay.png -compose Over -composite rounded_border.png

"""
