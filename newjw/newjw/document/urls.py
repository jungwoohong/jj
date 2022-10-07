from django.urls import path

from newjw.document.views import *

urlpatterns = [
    path('docReg/', docReg.as_view(),name="docReg" ),
    path('docSave/', docSave.as_view(),name="docSave" ),
    path('docUpload/', docUpload.as_view(),name="docUpload" ),
    path('docLoadList/', docLoadList.as_view(),name="docLoadList" ), 
    path('docLoadListData/', docLoadListData.as_view(),name="docLoadListData" ),  
    path('docJsonData/', docJsonData.as_view(),name="docJsonData" ),  
    path('docSearchList/', docSearchList.as_view(),name="docSearchList" ),
    path('docSearchListData/', docSearchListData.as_view(),name="docSearchListData" ),
    
]