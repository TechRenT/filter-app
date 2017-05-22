import html5lib
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from requests import exceptions

from . import forms
from . import functions
from filters.models import VRPage


@login_required
def qualify_form(request):
    form = forms.QualifyURLForm()
    if request.method == 'POST':
        form = forms.QualifyURLForm(request.POST, request.FILES)
        if form.is_valid():
            functions.handle_uploaded_file(request.FILES['file'])
            raw_urls = []
            has_keywords = []
            no_keywords = []
            urls_with_errors = []
            selected_vrpage = form.cleaned_data['vrpage']
            vrpage = get_object_or_404(VRPage, name=selected_vrpage)
            keywords = [str(keyword) for keyword in vrpage.keyword_set.all()]
            functions.csv_reader('media/qualify_urls.csv', raw_urls)
            for raw_url in raw_urls:
                try:
                    resp = requests.get(raw_url[0])
                except exceptions.RequestException:
                    urls_with_errors.append(raw_url)
                else:
                    if resp.ok:
                        content = resp.text.lower()
                        soup = BeautifulSoup(content, 'html5lib')
                        content = soup.get_text()
                        keywords_list = []
                        for keyword in keywords:
                            if keyword in content:
                                counter = content.count(keyword)
                                keywords_list.append([keyword, counter])
                        if keywords_list:
                            raw_url.insert(1, len(keywords_list))
                            raw_url.insert(2, keywords_list)
                            has_keywords.append(raw_url)
                        else:
                            no_keywords.append(raw_url)
                    else:
                        urls_with_errors.append(raw_url)
            functions.save_csv('media/has_keywords.csv', has_keywords)
            functions.save_csv('media/no_keywords.csv', no_keywords)
            functions.save_csv('media/urls_with_errors.csv', urls_with_errors)
            return render(request, 'qualify_urls/qualify_form.html', {'form': form,
                                                           'raw_urls': raw_urls,
                                                           'has_keywords': has_keywords,
                                                           'no_keywords': no_keywords,
                                                           'urls_with_errors': urls_with_errors,})
    return render(request, 'qualify_urls/qualify_form.html', {'form': form})

