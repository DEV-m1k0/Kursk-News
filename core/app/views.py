from django.shortcuts import render
from django.views import generic
import requests

class MainPageView(generic.TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = requests.get('http://127.0.0.1:8000/api/v1/posts/').json()
        return context
# Create your views here.
