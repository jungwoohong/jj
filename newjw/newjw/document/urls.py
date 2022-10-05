from django.urls import path

from newjw.document.views import *

urlpatterns = [
    path('docReg/', docReg.as_view(),name="docReg" ),
    path('docUpload/', docUpload.as_view(),name="docUpload" ),
    path('autocompleteData/', autocompleteData.as_view(),name="autocompleteData" ),
]