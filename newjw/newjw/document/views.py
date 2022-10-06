import json
from pprint import pprint
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
import pandas as pd
from django.utils import timezone
from .forms import postForm, dataCollectionForm, shareUserForm
from .models import post, data_collection, share_user
from datetime import datetime

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

class docSave(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        msg = "실패하였습니다."

        id          = request.POST.get('id')
        json_data   = request.POST.get('json_data')
        title       = request.POST.get('title')
        loginId     = request.user.username
        start_date  = datetime.strptime(request.POST.get('start_date'), "%Y.%m.%d")
        start_date  = timezone.make_aware(start_date)
        end_date    = datetime.strptime(request.POST.get('end_date'), "%Y.%m.%d")
        end_date    = timezone.make_aware(end_date)
                    
        arr = {"email": loginId,"json_data": json_data, "title": title,"start_date":start_date,"end_date": end_date}            
        form = postForm(arr)

        if form.is_valid():
            if id == '':
                # record = form.save()
                

                msg = "저장하였습니다."                    
            else :
                updateData = post.objects.get(id=id)
                updateData.json_data    = json_data
                updateData.title        = title
                updateData.start_date   = start_date
                updateData.end_date     = end_date
                updateData.save()
                msg = "수정하였습니다."                         

        retrunMsg = {"msg": msg, "form":form.errors}
        return JsonResponse(retrunMsg)        