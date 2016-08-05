from django.shortcuts import render
import csv

from . import forms
from .models import Filter

# Create your views here.
def filter_keywords_list(request):
    keywords = Filter.objects.all()
    return render(request, 'filters/keywords_list.html', {'keywords': keywords})

def handle_uploaded_file(f):
    with open('media/raw_urls.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def csv_reader(filename, list):
    """Open and read a csv file"""
    with open(filename, encoding="utf-8") as csvfile:
        read_csv = csv.reader(csvfile)
        for row in read_csv:
            list.append(row)

#def filter(refine_raw_urls, keywords, bad_urls, good_urls):
#    """Check each raw url if it contains bad keywords.
#    If it has, the raw url will be save to bad_urls list.
#    Otherwise it will be added to good_urls list"""
#    for url in refine_raw_urls:
#        while True:
#            for keyword in keywords:
#                if keyword in url[0]:
#                    bad_urls.append(url)
#                    break
#            if url not in bad_urls:
#                good_urls.append(url)
#            break

def filter(raw_urls, keywords, bad_urls, good_urls):
    """Check each raw url whether it's good or bad"""
    for url in raw_urls:
        if url[2] == "200 OK" and int(url[3]) >= 3:
            for keyword in keywords:
                if keyword in url[0]:
                    bad_urls.append(url)
                    break
            if url not in bad_urls:
                good_urls.append(url)
        else:
            bad_urls.append(url)

def save_csv(filename, list):
    """Save raw urls into a CSV file"""
    with open(filename, 'w', newline='', encoding="utf-8") as output:
        writer = csv.writer(output, delimiter=',')
        for url in list:
            writer.writerows([url])

def upload_file(request):
    if request.method == 'POST':
        form = forms.UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            raw_urls = []
            bad_urls = []
            good_urls = []
            keywords = [str(keyword) for keyword in Filter.objects.all()]
            csv_reader('media/raw_urls.csv', raw_urls)
#            refine_raw_urls = [url for url in raw_urls if url[2] == "200 OK"
#                       and int(url[3]) >= 3]
#            filter(refine_raw_urls, keywords, bad_urls, good_urls)
            filter(raw_urls, keywords, bad_urls, good_urls)
            save_csv('media/cleanurls.csv', good_urls)
            save_csv('media/badurls.csv', bad_urls)
            return render(request, 'filters/upload.html', {'form': form,
                                                           'raw_urls': raw_urls,
                                                           'good_urls': good_urls,
                                                           'bad_urls': bad_urls,
                                                           'keywords': keywords})
    else:
        form = forms.UploadFileForm()
    return render(request, 'filters/upload.html', {'form': form})

    
