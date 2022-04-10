import re
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView, ListView
from django.forms import (CharField, DateField, Form, IntegerField, ModelChoiceField, Textarea)


# Create your views here.

# def hello(request):
#   #s1 = request.GET.get('s1', '')
#   return render(
#     request, template_name='emailform.html',
#     context={}
#   )


class EmailViews(Form):
  email_from = CharField(max_length=128)
  email_to = CharField(max_length=128)
  email_subject = CharField(max_length=128)
  email_text = CharField(max_length=1024, widget=Textarea)

  def clean_email_text(self):
    # Force each sentence of the description to be capitalized.
    initial = self.cleaned_data['email_text']
    sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
    return '. '.join(sentence.capitalize() for sentence in sentences)

class EmailCreateView(FormView):
  template_name = 'emailform.html'
  form_class = EmailViews