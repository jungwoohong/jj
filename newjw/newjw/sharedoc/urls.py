from django.urls import path

from newjw.sharedoc.views import *

urlpatterns = [
    path('selectUserList/', selectUserList.as_view(),name="selectUserList" ),
    path('selectUserListData/', selectUserListData.as_view(), name="selectUserListData")
    
]