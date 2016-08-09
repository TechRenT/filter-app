from django.shortcuts import render

from . import forms
from .models import Filter
from . import functions


def filter_keywords_list(request):
    keywords = Filter.objects.all()
    return render(request, 'filters/keywords_list.html', {'keywords': keywords})

def upload_file(request):
    if request.method == 'POST':
        form = forms.UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            functions.handle_uploaded_file(request.FILES['file'])
            raw_urls = []
            bad_urls = []
            good_urls = []
            keywords = [str(keyword) for keyword in Filter.objects.all()]
            functions.csv_reader('media/raw_urls.csv', raw_urls)
            functions.filter(raw_urls, keywords, bad_urls, good_urls)
            functions.save_csv('media/cleanurls.csv', good_urls)
            functions.save_csv('media/badurls.csv', bad_urls)
            return render(request, 'filters/upload.html', {'form': form,
                                                           'raw_urls': raw_urls,
                                                           'good_urls': good_urls,
                                                           'bad_urls': bad_urls,
                                                           'keywords': keywords})
    else:
        form = forms.UploadFileForm()
    return render(request, 'filters/upload.html', {'form': form})

    
