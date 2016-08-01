from django.shortcuts import render

from .models import Filter

# Create your views here.
def filter_keywords_list(request):
    keywords = Filter.objects.all()
    return render(request, 'filters/keywords_list.html', {'keywords': keywords})
