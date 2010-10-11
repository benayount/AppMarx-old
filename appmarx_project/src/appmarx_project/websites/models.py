from django.db import models
from datetime import datetime, timedelta
import datetime
from appmarx_project.lib import *
# Website model

class Website(models.Model):
    name = models.CharField(max_length=255)
    URL = models.URLField(max_length=511)
    type = models.IntegerField()
    api_key = models.CharField(max_length=60, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def save(self):
        if not self.api_key:
            self.__make_api_key()
        super(Website, self).save()
        
    def __make_api_key(self):
        api_key = make_random_string(60)
        try:
            Website.objects.get(api_key=api_key)
        except Website.DoesNotExist:
            self.api_key = api_key
            return
        self.__make_api_key()
    
    def verify(self):
        self.is_verified = True
        self.verified_at = \
         datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        """ 
        TODO: maybe delete all record in table that have the same url
        and notify all unverified users associated to them about the verification
        """
    
    def __unicode__(self):
        return self.URL

# Website_Website Model

class Website_Website(models.Model):
    from_website = models.ForeignKey(Website, related_name='from')
    to_website = models.ForeignKey(Website, related_name='to')
    created_at = models.DateTimeField(auto_now_add=True)