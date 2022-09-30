from django.urls import path

from newjw.frame.views import *

urlpatterns = [
    path('reg/', frameViewReg.as_view() ),
    path('jsonSave/', frameViewSave.as_view(),name="frameViewSave" ),
]