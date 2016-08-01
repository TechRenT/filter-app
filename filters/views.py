from django.http import HttpResponse

from .models import Filter

# Create your views here.
def filter_keywords_list(request):
    keywords = Filter.objects.all()
    output = ", ".join([str(keyword) for keyword in keywords])
    return HttpResponse(output)
