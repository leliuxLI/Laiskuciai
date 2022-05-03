#from curses.textpad import Textbox
from calendar import week
from dataclasses import dataclass
import datetime
import re
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView, ListView
from django.forms import (BooleanField, CharField, DateField, EmailInput, Form, IntegerField, ModelChoiceField, PasswordInput, Textarea)
import smtplib # biblioteka susikalbėjimui su pašto serveriu
from email.message import EmailMessage
from .models import EmailSetings, MainTemplate
from django.contrib.auth.mixins import LoginRequiredMixin


class EmailServers(Form):
  smtp_host = CharField(max_length=200)
  smtp_port = IntegerField()
  email_login = CharField(max_length=200)
  email_pass =  CharField(max_length=200, widget=PasswordInput) 

class EmailTemplates(Form, LoginRequiredMixin):
  template_name = CharField(max_length=200)
  email_from = CharField(max_length=128)
  email_to = CharField(max_length=128, widget=EmailInput)
  email_subject = CharField(max_length=128)
  email_text = CharField(max_length=10000, widget=Textarea)
  email_start = DateField()
  email_end = DateField()
  week_monday = BooleanField()
  week_tuesday = BooleanField()
  week_wednesday = BooleanField()
  week_thursday = BooleanField()
  week_friday = BooleanField()
  week_saturday = BooleanField()
  week_sunday = BooleanField() 
  server_list = ModelChoiceField(queryset=EmailSetings.objects.all())
  # filter(user=self.request.user)) self susiziureti
    


def send_email(email_from, email_to, email_subject, email_text , sending_email, sending_pasword):
  email = EmailMessage()
  email['from'] = email_from
  email['to'] = email_to
  email['subject'] = email_subject
  email.set_content(email_text)

  with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    smtp.ehlo() # žiūrėkite, kaip į pasisveikinimą su serveriu
    smtp.starttls() # inicijuojame šifruotą kanalą
    smtp.login(sending_email, sending_pasword) # nurodome prisijungimo duomenis
    smtp.send_message(email) # išsiunčiame žinutę

class AllServerLists(ListView, LoginRequiredMixin):
    model = EmailSetings
    template_name = 'servers.html'

    def get_queryset(self):
        return EmailSetings.objects.filter(user=self.request.user)


class ServerCreateView(FormView, LoginRequiredMixin):
  template_name = 'serverform.html'
  form_class = EmailServers
  success_url = '/servers/'

  def form_valid(self, form):
    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
    user=self.request.user
    smtp_h = form.data['smtp_host']
    smtp_p = form.data['smtp_port']
    email_u = form.data['email_login']
    email_p = form.data['email_pass']

    server_item = EmailSetings(smtp_host=smtp_h, smtp_port=smtp_p, email_login=email_u, email_pass=email_p, user=user)
    server_item.save()

    return super().form_valid(form)

class AllTemplatesLists(ListView, LoginRequiredMixin):
    model = MainTemplate
    template_name = 'templates.html'

    def get_queryset(self):
        return MainTemplate.objects.filter(user=self.request.user)

class TemplateCreateView(FormView, LoginRequiredMixin):
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
    _email_start = form.data['email_start']
    _email_end = form.data['email_end']
    _week_monday = form.data['week_monday']
    _week_tuesday = form.data['week_tuesday']
    _week_wednesday = form.data['week_wednesday']
    _week_thursday = form.data['week_thursday']
    _week_friday = form.data['week_friday']
    _week_saturday = form.data['week_saturday']
    _week_sunday = form.data['week_sunday']
    _server_list = EmailSetings.objects.get(id=int(form.data['server_list']))
    _user=self.request.user

    _week = [_week_monday, _week_tuesday,_week_wednesday,_week_thursday,_week_friday, _week_saturday,_week_sunday]
    j = -1
    for i in _week:
      j += 1
      if i == "on": _week[j] = True
      else: _week[j] = False

    
  
    server_item = MainTemplate(user=_user,
                              template_name=_email_templ,
                               email_from=_email_from,
                               email_to=_email_to,
                               email_subject=_email_subject,
                               email_text=_email_text,
                               email_start = _email_start,
                               email_end = _email_end,
                               week_monday= _week[0],
                               week_tuesday = _week[1],
                               week_wednesday = _week[2],
                               week_thursday = _week[3],
                               week_friday = _week[4],
                               week_saturday = _week[5],
                               week_sunday = _week[6],
                               server_list=_server_list
                               )
    server_item.save()
    
    # import sched, time
    # s = sched.scheduler(time.time, time.sleep)
    # def print_time(a='default'):
    #       print("From print_time", time.time(), a)

    # def print_some_times():
    #   while True:
    #     print(time.time())
    #     s.enter(10, 1, print_time)
    #     s.enter(10, 1, time.sleep(1))
    #     s.enter(5, 2, print_time, argument=('positional',))
    #     s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
        
    #     s.run(blocking=False)
    
    #     print(time.time())
 
    # print_some_times()
    return super().form_valid(form)



def send_api(self):
  templates = ''
  current_week_day = datetime.datetime.today().weekday()
  current_day = datetime.datetime.today().strftime('%Y-%m-%d 00:00:00')
  current_week_day = 4

  if current_week_day == 0:
    current_filter = MainTemplate.objects.filter(week_monday=True).filter(email_end__gte=current_day).filter(email_start__lte=current_day)
  elif current_week_day == 1:
    current_filter = MainTemplate.objects.filter(week_tuesday=True).filter(email_end__gte=current_day).filter(email_start__lte=current_day)
  elif current_week_day == 2:
    current_filter = MainTemplate.objects.filter(week_wednesday=True).filter(email_end__gte=current_day).filter(email_start__lte=current_day)
  elif current_week_day == 3:
    current_filter = MainTemplate.objects.filter(week_thursday=True).filter(email_end__gte=current_day).filter(email_start__lte=current_day)
  elif current_week_day == 4:
    current_filter = MainTemplate.objects.filter(week_friday=True).filter(email_end__gte=current_day).filter(email_start__lte=current_day)
  elif current_week_day == 5:
    current_filter = MainTemplate.objects.filter(week_saturday=True).filter(email_end__gte=current_day).filter(email_start__lte=current_day)
  elif current_week_day == 6:
    current_filter = MainTemplate.objects.filter(week_sunday=True).filter(email_end__gte=current_day).filter(email_start__lte=current_day)
  else:
    return

  for ob in current_filter:
    smtp_login = ob.server_list.email_login
    smtp_pass = ob.server_list.email_pass
    send_email(ob.email_from, ob.email_to, ob.email_subject, ob.email_text, smtp_login, smtp_pass)
    templates += ob.template_name + ','
  return HttpResponse({templates})