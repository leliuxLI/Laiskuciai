#from curses.textpad import Textbox
import re
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView, ListView
from django.forms import (BooleanField, CharField, DateField, EmailInput, Form, IntegerField, ModelChoiceField, PasswordInput, Textarea)
import smtplib # biblioteka susikalbėjimui su pašto serveriu
from email.message import EmailMessage
from .models import EmailSetings, MainTemplate


class EmailServers(Form):
  smtp_host = CharField(max_length=200)
  smtp_port = IntegerField()
  email_login = CharField(max_length=200)
  email_pass =  CharField(max_length=200, widget=PasswordInput) 

class EmailTemplates(Form):
  template_name = CharField(max_length=200)
  email_from = CharField(max_length=128)
  email_to = CharField(max_length=128, widget=EmailInput)
  email_subject = CharField(max_length=128)
  email_text = CharField(max_length=10000, widget=Textarea)
  week_monday = BooleanField()
  server_list = ModelChoiceField(queryset=EmailSetings.objects.all()) 
    


# class EmailViews(Form):
#   email_from = CharField(max_length=128)
#   email_to = CharField(max_length=128, widget=EmailInput)
#   email_subject = CharField(max_length=128)
#   email_text = CharField(max_length=10000)
#   sending_email = CharField(max_length=128, widget=EmailInput)
#   sending_pasword = CharField(max_length=128, widget=PasswordInput)
#   week_monday = BooleanField()



#   def send_email(self, email_from, email_to, email_subject, email_text , sending_email, sending_pasword):
#     email = EmailMessage()
#     email['from'] = email_from
#     email['to'] = email_to
#     email['subject'] = email_subject
#     email.set_content(email_text)

#     with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
#         smtp.ehlo() # žiūrėkite, kaip į pasisveikinimą su serveriu
#         smtp.starttls() # inicijuojame šifruotą kanalą
#         smtp.login(sending_email, sending_pasword) # nurodome prisijungimo duomenis
#         smtp.send_message(email) # išsiunčiame žinutę

class AllServerLists(ListView):
    model = EmailSetings
    template_name = 'servers.html'

    def get_queryset(self):
        return EmailSetings.objects.filter()


class ServerCreateView(FormView):
  template_name = 'serverform.html'
  form_class = EmailServers
  success_url = '/servers/'
  
  def form_valid(self, form):
    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
    smtp_h = form.data['smtp_host']
    smtp_p = form.data['smtp_port']
    email_u = form.data['email_login']
    email_p = form.data['email_pass']

    server_item = EmailSetings(smtp_host=smtp_h, smtp_port=smtp_p, email_login=email_u, email_pass=email_p)
    server_item.save()

    return super().form_valid(form)

class AllTemplatesLists(ListView):
    model = MainTemplate
    template_name = 'templates.html'

    def get_queryset(self):
        return MainTemplate.objects.filter()

class TemplateCreateView(FormView):
  template_name = 'templateform.html'
  form_class = EmailTemplates
  success_url = '/templates/'

  def form_valid(self, form):
    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
    _email_templ = form.data['template_name']
    _email_from = form.data['email_from']
    _email_to = form.data['email_to']
    _email_subject = form.data['email_subject']
    _email_text = form.data['email_text']
    _week_monday = form.data['week_monday']
    _server_list = EmailSetings.objects.get(id=int(form.data['server_list']))
 
    if _week_monday == "on":
      _week_monday = True
    else:
      _week_monday = False
    
  
    server_item = MainTemplate(template_name=_email_templ,
                               email_from=_email_from,
                               email_to=_email_to,
                               email_subject=_email_subject,
                               email_text=_email_text,
                               week_monday=_week_monday,
                               server_list=_server_list
                               )
    server_item.save()

    return super().form_valid(form)