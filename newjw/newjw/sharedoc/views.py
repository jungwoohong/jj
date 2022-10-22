from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import Http404, JsonResponse
from django.core import serializers
from django.db.models import Subquery
from .models import *
# from newjw.sharedoc.models import *
import json

class selectUserList(LoginRequiredMixin, View):

    def get(self, request):
                    
        return render(request, 'sharedoc/selectUserList.html')

class selectUserListData(LoginRequiredMixin, View):

    def get(self, request):

        id = request.GET.get('id')
        context = {}
    
        groupset = group_test_table.objects.filter(parent_code=id)
        group        = serializers.serialize("json", groupset)
        group        = json.loads(group)

        userset = user_test_table.objects.filter(dept_code__in=Subquery(groupset.values('dept_code')))
        user        = serializers.serialize("json", userset)
        user        = json.loads(user)

        context = {
            "group":group,
            "user":user
        }
    
        return JsonResponse(context) 
        # queryset = user_test_table.objects.select_related('dept_code').all()
        # data        = serializers.serialize("json", queryset)
        # data        = json.loads(data)

        # queryset = user_test_table.objects.select_related('dept_code')
        # print(str(queryset.query))
        # for a in queryset:
        #     print(a.dept_code.dept_name)

        # return render(request, 'board/reg.html', context)

        