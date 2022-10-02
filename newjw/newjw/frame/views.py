from pprint import pprint
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from core.views import DatatablesServerSideView

import json
from .models import post
from .forms import postForm


class frameViewReg(LoginRequiredMixin, View):

    def get(self, request):

        return render(request, 'frame/reg.html')


class frameViewSave(LoginRequiredMixin, View):

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(frameViewSave, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        msg = "실패하였습니다."

        if request.method == 'POST':
            json_data   = request.POST.get('data')
            title       = request.POST.get('title')
            loginId     = request.user.username
            arr = {"email": loginId,"json_data": json_data, "title": title }
            print(arr)
            form = postForm(arr)

            if form.is_valid():
                record = form.save()
                msg = "저장하였습니다."

        retrunMsg = {"msg": msg}
        return JsonResponse(retrunMsg)


class frameLoadList(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'frame/frameList.html')


class frameLoadListData(LoginRequiredMixin, DatatablesServerSideView):

    model = post
    columns = ['id','title','email', 'create_date']
    searchable_columns = ['title','email']
    #foreign_fields = {'create': 'create__date'}

    def get_initial_queryset(self):
        qs = super(frameLoadListData, self).get_initial_queryset()
        return qs.filter(email__isnull=False)