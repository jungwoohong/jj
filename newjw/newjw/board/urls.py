from django.urls import path

from newjw.board.views import *

urlpatterns = [
    path('', index.as_view()),
    path('getBoardListData/',getBoardListData.as_view(), name="getBoardListData"),
    path('postReg/',postReg.as_view(), name="postReg"),
    path('postSave/',postSave.as_view(), name="postSave")
]