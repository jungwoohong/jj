from django.urls import path

from newjw.board.views import *

urlpatterns = [
    path('', index.as_view()),
    path('getBoardList',getBoardList.as_view()),
    path('postReg',postReg.as_view(), name="postReg"),
]