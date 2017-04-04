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


class QualifyURLForm(forms.Form):
    raw_url = forms.URLField()


class LinkedinProfileForm(forms.ModelForm):
    class Meta:
        model = models.LinkedinProfile
        fields = [
            'profile_link',
        ]

    def clean(self):
        cleaned_data = super(LinkedinProfileForm, self).clean()
        profile_link = cleaned_data.get("profile_link")

        profile_list = [str(profile) for profile in models.LinkedinProfile.objects.all()]

        if profile_link in profile_list:
            raise forms.ValidationError("This profile already exist in our database!")

