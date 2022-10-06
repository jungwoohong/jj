from django.urls import path

from newjw.document.views import *

urlpatterns = [
    path('docReg/', docReg.as_view(),name="docReg" ),
    path('docSave/', docSave.as_view(),name="docSave" ),
    path('docUpload/', docUpload.as_view(),name="docUpload" ), 
]