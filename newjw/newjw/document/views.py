import json
from pprint import pprint
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
import pandas as pd


class docReg(LoginRequiredMixin, View):

    def get(self, request):

        context = {}
        id = request.GET.get('id')

        if(id):
            # data = get_object_or_404(post, id=id)
            # context = {"data":data}
            print('')

        return render(request, 'document/reg.html', context)


class docUpload(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'document/upload.html')

    def post(self, request):

        file        = request.FILES['file1']
        file_name   = file.name
        pd_read     = ""

        if(file_name.find(".csv") == -1) :
            pd_read = pd.read_excel(file)
        else :
            pd_read = pd.read_csv(file)   

        rs = pd_read.to_json(orient="values")
        parsed = json.loads(rs)

        retrunMsg = {"data": parsed}

        return JsonResponse(retrunMsg)
