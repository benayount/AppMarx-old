from django.db import models
from appmarx_project.websites.models import Website
from appmarx_project.lib import *
from appmarx_project.defines import *
from django.core.mail import EmailMessage
from datetime import datetime
import datetime

import hashlib

# User model

class User(models.Model):
    email = models.EmailField(unique=True)
    encrypted_password = models.CharField(max_length=40)
    fullname = models.CharField(max_length=64)
    type = models.IntegerField()
    salt = models.CharField(max_length=16, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def set_password(self, password):
        self.__encrypt_password(password)
        
    def get_password(self):
        return self.password
    
    password = property(None, set_password)
    
    def __encrypt_password(self, password):
        if not self.salt:
            self.salt = make_random_string(16)
        self.encrypted_password = hashlib.sha1(self.salt+password).hexdigest()
        
    def __unicode__(self):
            return self.email
        
# User_Activation model        

class User_Activation(models.Model):
    user = models.ForeignKey(User, unique=True)
    activation_code = models.CharField(max_length=32, blank=True, unique=True)
    activated_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self):
        if not self.activation_code:
            self.__make_activation_code()
        super(User_Activation, self).save()
        # sending the email, actually an observer would be a better choice for that
        activation_mail = EmailMessage(EMAIL_ACTIVATION_SUBJECT, "Welcome abroad "+self.user.email \
                  +".\n Please click the link below to activate your account:\n http://appmarx.com/users/activate/"+\
                  self.activation_code+"\n\nThanks,\nThe AppAarx team", EMAIL_ACTIVATION_SENDER,
                  to=[self.user.email])
        activation_mail.send()
        
    def __make_activation_code(self):
        activation_code = make_random_string(32)
        try:
            User_Activation.objects.get(activation_code=activation_code)
        except User_Activation.DoesNotExist:
            self.activation_code = activation_code
            return
        self.__make_activation_code()
    
    def activate(self):
        self.activated_at = \
         datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
             
    def __unicode__(self):
        return self.activation_code

# Website_User model, Many users to Website for now

class User_Website(models.Model):
    website = models.ForeignKey(Website)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.user.__unicode__()+" <--> "+self.website.__unicode__()
    
# User_AutoLogin

class User_AutoLogin(models.Model):
    user = models.ForeignKey(User)
    remember_token = models.CharField(max_length=32, blank=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self):
        if not self.remember_token:
            self.remember_token = make_random_string(32)
            
        # keep MAX_AUTOLOGIN maximum auto logins, and clean expired ones
        now = datetime.datetime.now()
        for ua in User_AutoLogin.objects.filter(user=self.user):
            if ua.expires_at < now:
                ua.delete()
                
        super(User_AutoLogin, self).save()
    
    def __unicode__(self):
        return self.remember_token
    