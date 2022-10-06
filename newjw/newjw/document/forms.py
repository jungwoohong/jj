from django import forms
from .models import post, data_collection, share_user

class postForm(forms.ModelForm):
    class Meta:
        model = post
        fields = '__all__'    

class dataCollectionForm(forms.ModelForm):
    class Meta:
        model = data_collection
        fields = '__all__'   

class shareUserForm(forms.ModelForm):
    class Meta:
        model = share_user
        fields = '__all__'                   