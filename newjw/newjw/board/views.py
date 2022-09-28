from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import post
import json

class index(LoginRequiredMixin, View):    
    def get(self, request):
        return render(request, 'board/boardList.html')

class getBoardList(LoginRequiredMixin, View):

    def get(self, request):
        posts = post.objects.all()
        post_list = []
        for a in posts:
            post_list.append({
                'id':a.id,
                'title':a.title,
                'user_id':a.user_id,
                'registered_date':a.registered_date,
                'view_count':a.view_count
            })
        # postserial = serializers.serialize('json', posts)
        # rs = {'data':json.loads(postserial)}
        return JsonResponse({'data':post_list}, safe=False)
          