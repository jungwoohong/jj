from django.urls import path

from newjw.frame.views import *

urlpatterns = [
    path('reg/', frameViewReg.as_view(),name="frameReg" ),
    path('jsonSave/', frameViewSave.as_view(),name="frameViewSave" ),
    path('frameLoadList/', frameLoadList.as_view(),name="frameLoadList" ),
    path('frameLoadListData/', frameLoadListData.as_view(),name="frameLoadListData" ),
    path('frameJsonData/', frameJsonData.as_view(),name="frameJsonData" ),
    path('docToSearchList/', docToSearchList.as_view(),name="docToSearchList" ),
    path('docToSearchListData/', docToSearchListData.as_view(),name="docToSearchListData" ),
    path('mailtest/', mailtest.as_view(),name="mailtest" ),
    
]