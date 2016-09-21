from django import forms

from . import models

class UploadFileForm(forms.Form):
    file = forms.FileField()
    shepard_urls = forms.BooleanField(initial=True, required=False)


class KeywordForm(forms.ModelForm):
    class Meta:
        model = models.Filter
        fields = [
            'order',
            'keyword'
        ]


class UrlToDomainForm(forms.Form):
    input_urls = forms.CharField(widget=forms.Textarea)
