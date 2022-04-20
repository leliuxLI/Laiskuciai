import re
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView, ListView
from django.forms import (CharField, DateField, EmailInput, Form, IntegerField, ModelChoiceField, PasswordInput, Textarea)
import smtplib # biblioteka susikalbėjimui su pašto serveriu
from email.message import EmailMessage



class EmailViews(Form):
  email_from = CharField(max_length=128)
  email_to = CharField(max_length=128)
  email_subject = CharField(max_length=128)
  email_text = CharField(max_length=1024, widget=EmailMessage)
  # sending_email = CharField(max_length=128)
  # sending_pasword = CharField(max_length=128, widget=PasswordInput)



  def send_email(self, email_from, email_to, email_subject, email_text , sending_email, sending_pasword):
    email = EmailMessage()
    email['from'] = email_from
    email['to'] = email_to
    email['subject'] = email_subject

    email.set_content(email_text)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo() # žiūrėkite, kaip į pasisveikinimą su serveriu
        smtp.starttls() # inicijuojame šifruotą kanalą
        smtp.login('krekeris@gmail.com', MKrambambuolis1) # nurodome prisijungimo duomenis
        smtp.send_message(email) # išsiunčiame žinutę

  
class EmailCreateView(FormView):
  template_name = 'emailform.html'
  form_class = EmailViews
  success_url = '/thanks/'

  def form_valid(self, form):
    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
    email_from = form.data['email_from']
    email_to = form.data['email_to']
    email_subject = form.data['email_subject']
    email_text = form.data['email_text']
    
    form.send_email(email_from, email_to, email_subject, email_text)
    return super().form_valid(form)