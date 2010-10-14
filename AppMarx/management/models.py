from django.db import models
from helpers import make_random_string
from defines import *
from django.core.mail import EmailMessage
import datetime

import hashlib
import sys

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
    
    password = property(None, set_password)
    
    def __encrypt_password(self, password):
        if not self.salt:
            self.salt = make_random_string(16)
        self.encrypted_password = hashlib.sha1(self.salt+password).hexdigest()
        
    def __unicode__(self):
            return self.email
        
# Forget password model -- records here are for users, granted
# to change their password once providing token field

class User_ForgetPassword(models.Model):
    user = models.ForeignKey(User, unique=True)
    token = models.CharField(max_length=32, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self):
        self.__make_token()
        super(User_ForgetPassword, self).save()
        
        # sending the email
        self.send_forget_password_email()
        
    def __make_token(self):
        token = make_random_string(32)
        try:
            User_ForgetPassword.objects.get(token=token)
        except User_ForgetPassword.DoesNotExist:
            self.token = token
            return
        self.__make_token()
    
    def send_forget_password_email(self):
        # send the email
        forget_password_mail = EmailMessage("Forget password", self.user.email \
                      +".\n Click the link below to change your password:\n http://localhost:8000/management/change_password/"+\
                      self.token+"\n\nThanks,\nThe AppAarx team", APPMARX_ACCOUNTS_EMAIL,
                      to=[self.user.email])
        forget_password_mail.send()
    
    def __unicode__(self):
        return self.token


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
        
        # sending the email
        self.send_activation_mail()
        
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
             
    
    def send_activation_mail(self):
        activation_mail = EmailMessage(EMAIL_ACTIVATION_SUBJECT, "Welcome abroad "+self.user.email \
                      +".\n Please click the link below to activate your account:\n http://localhost:8000/management/activate/"+\
                      self.activation_code+"\n\nThanks,\nThe AppAarx team", APPMARX_ACCOUNTS_EMAIL,
                      to=[self.user.email])
        activation_mail.send()
    
    def __unicode__(self):
        return self.activation_code

# Website model

class Website(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511,blank=True)
    favicon32 = models.ImageField(upload_to='favicons/%Y/%m/%d/')
    favicon48 = models.ImageField(upload_to='favicons/%Y/%m/%d/')
    favicon64 = models.ImageField(upload_to='favicons/%Y/%m/%d/')
    URL = models.URLField(max_length=511)
    type = models.IntegerField()
    api_key = models.CharField(max_length=60,blank=True,unique=True)
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
            
        # clean any expired autologins of this user
        now = datetime.datetime.now()
        for ua in User_AutoLogin.objects.filter(user=self.user):
            if ua.expires_at < now:
                ua.delete()
                
        super(User_AutoLogin, self).save()
    
    def __unicode__(self):
        return self.remember_token

# Website_Website Model

class Website_Website(models.Model):
    from_website = models.ForeignKey(Website, related_name='from')
    to_website = models.ForeignKey(Website, related_name='to')
    created_at = models.DateTimeField(auto_now_add=True)

class Website_Images(models.Model):
    image = models.ImageField(upload_to='favicons/%Y/%m/%d')
    website = models.ForeignKey(Website)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    