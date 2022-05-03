from django.urls import path
from django.contrib.auth.decorators import login_required

from  . import views

urlpatterns = [
  path('template_form/', login_required(views.TemplateCreateView.as_view()), name='templateform'),
  path('server_form/', login_required(views.ServerCreateView.as_view()), name='serverform'),
  path('servers/', login_required(views.AllServerLists.as_view()), name='servers'),
  path('', login_required(views.AllTemplatesLists.as_view()), name='index'),
  path('send/', views.send_api, name='index'),
]