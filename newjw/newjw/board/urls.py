from django.urls import path

from newjw.board.views import *

urlpatterns = [
    path('', index.as_view(), name="indexPage"),
    path('getBoardListData/',getBoardListData.as_view(), name="getBoardListData"),
    path('postReg/',postReg.as_view(), name="postReg"),
    path('postSave/',postSave.as_view(), name="postSave"),
    path('postDetailView/',postDetailView.as_view(), name="postDetailView"),
    path('fileDownload/<int:id>',fileDownload.as_view(), name="fileDownload" ),
    path('fileDelete/', fileDelete.as_view(), name="fileDelete")
]