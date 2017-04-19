from django import forms

VR_PAGES = (
    ('History of Scrapbooking', 'History of Scrapbooking'),
    ('Kaizen', 'Kaizen'),
    ('Travel Warnings and Alerts', 'Travel Warnings and Alerts'),
    ('Paper Preservation', 'Paper Preservation'),
)

class QualifyURLForm(forms.Form):
    file = forms.FileField()
    vrpage = forms.ChoiceField(choices=VR_PAGES)