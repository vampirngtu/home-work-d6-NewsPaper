
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, TemplateView
from .forms import BaseRegisterForm
from django.shortcuts import redirect 


class BaseRegisterView(CreateView):
   model = User
   form_class = BaseRegisterForm
   success_url = '/news/'

