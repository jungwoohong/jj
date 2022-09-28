from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from .models import post

@login_required
def index(request):
    posts = post.objects.all()
    return render(request, 'board/boardList.html',{'posts':posts})