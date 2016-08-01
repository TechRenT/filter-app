from django import forms

class FilterForm(forms.Form):
    raw_url = forms.CharField(widget=forms.Textarea)


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class UploadFileForm(forms.Form):
    file = forms.FileField()