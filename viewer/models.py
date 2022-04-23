from django.db import models
import datetime
# Create your models here.
class EmailSetings(models.Model):
    smtp_host = models.CharField(max_length=200)
    smtp_port = models.IntegerField()
    email_login = models.CharField(max_length=200)
    email_pass = models.CharField(max_length=200) 
    
    def __str__(self):
        return self.smtp_host + ':' + str(self.smtp_port) + ' [' + self.email_login + ']'

class MainTemplate(models.Model):
    template_name = models.CharField(max_length=200)
    email_from = models.CharField(max_length=128)
    email_to = models.EmailField(max_length=128)
    email_subject = models.CharField(max_length=128)
    email_text = models.TextField()
    email_start = models.DateTimeField(auto_now_add=True, blank=True)
    email_end = models.DateTimeField(auto_now_add=True, blank=True)
    week_monday = models.BooleanField(default=False)
    week_tuesday = models.BooleanField(default=False)
    week_wednesday = models.BooleanField(default=False)
    week_thursday = models.BooleanField(default=False)
    week_friday = models.BooleanField(default=False)
    week_saturday = models.BooleanField(default=False)
    week_sunday = models.BooleanField(default=False)
    server_list = models.ForeignKey(EmailSetings, on_delete=models.CASCADE)    

class UserList(models.Model):
    user_name = models.CharField(max_length=200)
    user_email = models.CharField(max_length=200)
    template_list = models.ForeignKey(MainTemplate, on_delete=models.CASCADE)





