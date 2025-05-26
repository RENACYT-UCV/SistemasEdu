from django import forms

class VideoForm(forms.Form):
    nombre = forms.CharField(max_length=255)
    archivo = forms.FileField()
