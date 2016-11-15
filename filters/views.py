import tldextract
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView, UpdateView, DeleteView
)

from . import forms
from .models import Filter
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
    return render(request, 'filters/url_to_domain.html', {'form': form})


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

