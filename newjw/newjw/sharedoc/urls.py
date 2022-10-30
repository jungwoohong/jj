from django.urls import path

from newjw.sharedoc.views import *

urlpatterns = [
    path('selectUserList/', selectUserList.as_view(),name="selectUserList" ),
    path('selectUserListData/', selectUserListData.as_view(), name="selectUserListData"),
    path('myWriteList/', myWriteList.as_view(), name="myWriteList"),
    path('myWriteListData/', myWriteListData.as_view(), name="myWriteListData"),    
    path('shareDocDetail/', shareDocDetail.as_view(), name="shareDocDetail"),
    path('shareDocSave/', shareDocSave.as_view(), name="shareDocSave"),
    path('shareDocSearchList/', shareDocSearchList.as_view(), name="shareDocSearchList"),
    path('shareDocSearchListData/', shareDocSearchListData.as_view(), name="shareDocSearchListData"),     
    path('shareDocJsonData/', shareDocJsonData.as_view(), name="shareDocJsonData"),
    path('oriDocStatusChk/', oriDocStatusChk.as_view(), name="oriDocStatusChk")
       
]