from django import forms
from .models import post, user, data_collection, excel_json_data

class sharePostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = '__all__'    

class shareUserForm(forms.ModelForm):
    class Meta:
        model = user
        fields = '__all__'   

class shareDataCollectionForm(forms.ModelForm):
    class Meta:
        model = data_collection
        fields = '__all__'   

class shareExcelJsonDataForm(forms.ModelForm):
    class Meta:
        model = excel_json_data
        fields = '__all__'