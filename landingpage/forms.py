# landingpage/forms.py
from django import forms

class PredictionForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(min_value=0)
    gender = forms.ChoiceField(choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')])
    occupation = forms.CharField(max_length=100)
    event = forms.ChoiceField(choices=[('Weekend', 'Weekend'), ('Weekday', 'Weekday')])
