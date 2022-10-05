from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import json

from .models import post


class index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'board/boardList.html')


class getBoardList(LoginRequiredMixin, View):

    def get(self, request):

        datatables = request.GET
        draw = int(datatables.get('draw'))
        start = int(datatables.get('start'))
        length = int(datatables.get('length'))
        search = datatables.get('search[value]')
        print("draw : ", draw, "start : ", start, "length : ", length)
        posts = post.objects.all()
        posts_total = posts.count()
        posts_filtered = posts_total
        print("posts_total : " , posts_total)

        if search:
            posts = post.objects.filter(  # or 같은 조건문으로 사용할 때 Q()
                Q(id__icontains=search) |
                Q(title__icontains=search) |
                Q(user_id__icontains=search)
            )
            posts_total = posts.count()
            posts_filtered = posts_total

        paginator = Paginator(posts, length)
        page_number = int(start / length) + 1

        try:
            object_list = paginator.page(page_number).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(1).object_list
        
        print(page_number)

        data = [{
                'id': ol.id,
                'title': ol.title,
                'user_id': ol.user_id,
                'registered_date': ol.registered_date,
                'view_count': ol.view_count
			    } for ol in object_list
		    ]

        return JsonResponse({
            'draw': draw,
			'recordsTotal': posts_total,
			'recordsFiltered': posts_filtered,
            'data':data}, safe=False)


class postReg(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'board/reg.html')