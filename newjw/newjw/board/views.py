from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    post_data = Board.object.all();
    return render(request, 'board/boardList.html',post_data)