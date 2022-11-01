from django.urls import path

from newjw.cal.views import *

urlpatterns = [
    path('scheduleChk/', scheduleChk.as_view(),name="scheduleChk" ),
]