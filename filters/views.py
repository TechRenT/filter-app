import requests
import tldextract
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView, UpdateView, DeleteView
)
from requests import exceptions

from . import forms
from .models import Filter, Keyword, VRPage, LinkedinProfile
from . import functions
from . import mixins


@login_required
def filter_keywords_list(request):
    keywords = Filter.objects.all()
    return render(request, 'filters/keywords_list.html', {'keywords': keywords})


@login_required
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
            if form.cleaned_data['shepard_urls'] == True:
                functions.filter_shepard(raw_urls, keywords, bad_urls, good_urls)
            else:
                functions.filter_arrow(raw_urls, keywords, bad_urls, good_urls)
            functions.save_csv('media/cleanurls.csv', good_urls)
            functions.save_csv('media/badurls.csv', bad_urls)
            return render(request, 'filters/upload.html', {'form': form,
                                                           'raw_urls': raw_urls,
                                                           'good_urls': good_urls,
                                                           'bad_urls': bad_urls,})
    else:
        form = forms.UploadFileForm()
    return render(request, 'filters/upload.html', {'form': form})


@login_required
def keyword_create(request):
    form = forms.KeywordForm()
    if request.method == 'POST':
        form = forms.KeywordForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('filter:keywords'))
    return render(request, 'filters/keyword_form.html', {'form': form})


@login_required
def keyword_edit(request, keyword_pk):
    keyword = get_object_or_404(Filter, pk=keyword_pk)
    form = forms.KeywordForm(instance=keyword)
    if request.method == 'POST':
        form = forms.KeywordForm(instance=keyword, data=request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('filter:keywords'))
    return render(request, 'filters/keyword_form.html', {'form': form})


@login_required
def keyword_delete(request, keyword_pk):
    keyword = get_object_or_404(Filter, pk=keyword_pk).delete()
    return HttpResponseRedirect(reverse('filter:keywords'))


@login_required
def url_to_domain(request):
    form = forms.UrlToDomainForm()
    if request.method == 'POST':
        form = forms.UrlToDomainForm(request.POST)
        if form.is_valid():
            urls = form.cleaned_data['input_urls'].splitlines()
            domain_list = []
            for url in urls:
                domain = tldextract.extract(url).registered_domain
                domain_list.append(domain)
            return render(request, 'filters/url_to_domain.html', {'form': form, 'domain_list': domain_list})
    return render(request, 'filters/url_to_domain.html', {'form': form,})


@login_required
def qualify_url_list(request):
    vrpages = VRPage.objects.all()
    return render(request, 'filters/qualify_url_list.html', {'vrpages': vrpages})


@login_required
def qualify_url(request, vrpage_pk):
    form = forms.QualifyURLForm()
    vrpage = get_object_or_404(VRPage, pk=vrpage_pk)
    if request.method == 'POST':
        form = forms.QualifyURLForm(request.POST)
        if form.is_valid():
            keywords = [str(keyword) for keyword in Keyword.objects.filter(vrpage=vrpage_pk)]
            keywords_present = []
            raw_url = form.cleaned_data['raw_url']
            try:
                resp = requests.get(raw_url)
            except exceptions.ContentDecodingError:
                messages.add_message(request, messages.ERROR,
                    'ContentDecodingError occurred!')
            else:
                content = resp.text.lower()
                soup = BeautifulSoup(content, 'html.parser')
                content = soup.get_text()
                if resp.ok:
                    for keyword in keywords:
                        if keyword in content:
                            counter = content.count(keyword)
                            keywords_present.append([keyword, counter])
                    if keywords_present:
                        messages.add_message(request, messages.SUCCESS,
                            "found.")
                    else:
                        messages.add_message(request, messages.INFO,
                            'No keywords found.')
                else:
                    messages.add_message(request, messages.ERROR,
                        'An error occurred. Error code: {}'.format(resp.status_code))

                return render(request, 'filters/qualify_url.html',
                              {'form': form, 'keywords_present': keywords_present, 'vrpage': vrpage})
    return render(request, 'filters/qualify_url.html', {'form': form, 'vrpage': vrpage})


class KeywordListView(LoginRequiredMixin, ListView):
    context_object_name = "keywords"
    model = Filter


class KeywordCreateView(LoginRequiredMixin, mixins.PageTitleMixin, CreateView):
    fields = ("order", "keyword")
    model = Filter
    page_title = "Create Keyword"


class KeywordUpdateView(LoginRequiredMixin, mixins.PageTitleMixin, UpdateView):
    fields = ("order", "keyword")
    model = Filter

    def get_page_title(self):
        obj = self.get_object()
        return "Edit {}".format(obj.keyword)


class KeywordDeleteView(LoginRequiredMixin, DeleteView):
    model = Filter
    success_url = reverse_lazy("filter:keywords_cbv")


@login_required
def linkedin_profile_list(request):
    linkedin_profiles = LinkedinProfile.objects.all()
    return render(request, 'filters/linkedin_profile_list.html', {'linkedin_profiles': linkedin_profiles})

@login_required
def linkedin_profile_create(request):
    form = forms.LinkedinProfileForm()
    linkedin_profiles = len(LinkedinProfile.objects.all())
    if request.method == 'POST':
        form = forms.LinkedinProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                'LinkedIn profile has been successfully added!')
            return HttpResponseRedirect(reverse('filter:linkedin'))
    return render(request, 'filters/linkedin.html', {'form': form, 'profiles': linkedin_profiles})

