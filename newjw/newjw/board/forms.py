from django import forms
from .models import *

class postForm(forms.ModelForm):
    class Meta:
        model = post
        fields = '__all__'    

class uploadFileForm(forms.ModelForm):
    class Meta:
        model = upload_file
        fields = '__all__'    