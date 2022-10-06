from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import json
from core.views import DatatablesServerSideView

from .forms import postForm
from .models import post


class index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'board/boardList.html')


class getBoardListData(LoginRequiredMixin, DatatablesServerSideView):

    model = post
    columns = ['id','title','user_id', 'registered_date', 'view_count']
    searchable_columns = ['title']
    #foreign_fields = {'create': 'create__date'}

    def get_initial_queryset(self):
        qs = super(getBoardListData, self).get_initial_queryset()
        return qs.filter(id__isnull=False)


class postReg(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'board/reg.html')

class postSave(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        msg = "실패하였습니다."

        id          = request.POST.get('id')
        category    = request.POST.get('category')
        title       = request.POST.get('title')
        content     = request.POST.get('content')
        loginId     = request.user.username   

        arr = {"user_id": loginId, "category": category, "title": title,"content": content }
        form = postForm(arr)

        if form.is_valid():
            if id == '':
                record = form.save()
                msg = "저장하였습니다."
            else:
                updateData = post.objects.get(id=id)
                updateData.title        = title
                updateData.content        = content
                updateData.save()
                msg = "수정하였습니다."                         

        retrunMsg = {"msg": msg}
        
        return JsonResponse(retrunMsg)   

class postDetailView(LoginRequiredMixin, View):
    def get(self, request):
        
        id = request.GET.get('id')
        if id != '':
            try:
                rs = post.objects.get(id=id)
                context = {
                    'rs' : rs,
                }
                return render(request, 'board/detail.html', context)
            except post.DoesNotExist:
                return           


        return render(request, 'board/boardList.html')