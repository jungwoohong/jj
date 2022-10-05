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