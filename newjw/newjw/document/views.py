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
from core.views import DatatablesServerSideView

class docReg(LoginRequiredMixin, View):

    def get(self, request):

        context = {}
        id = request.GET.get('id')

        if(id):
             data = get_object_or_404(post, id=id)
             context = {"data":data}

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

                #post 저장
                record = form.save()
                
                # 데이터 저장
                jsonList = json.loads(json_data)
                cell_row = 0
                cell_line = 0

                for forData in jsonList :
                    cell_row = cell_row+1
                    cell_line = 0
                    for rs in forData :
                        cell_line = cell_line+1
                        cell_type = "cell"
                        if cell_row == 1 or cell_row == 2 :
                            cell_type = "header"

                        arrDataCollection = {"post":record.id,"cell_row":cell_row,"cell_line":cell_line,"data":rs,"cell_type":cell_type} 
                        formDataCollection = dataCollectionForm(arrDataCollection)

                        if formDataCollection.is_valid():
                            formDataCollection.save()

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

class docLoadList(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'document/docList.html')

class docLoadListData(LoginRequiredMixin, DatatablesServerSideView):

    model = post
    columns = ['id','title','email', 'start_date','end_date','create_date']
    searchable_columns = ['title','email']

    def get_initial_queryset(self):
        qs = super(docLoadListData, self).get_initial_queryset()
        return qs.filter(email__isnull=False)

class docJsonData(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        data = ''
        id          = request.POST.get('id')
        rs          = get_object_or_404(post, id=id)
        json_data   = rs.json_data
        rep_data    = json_data.replace("'", "\"")
        data        = json.loads(rep_data)
            
        retrunMsg = {"data": data}
        return JsonResponse(retrunMsg)            


class docSearchList(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'document/docSearchList.html')

class docSearchListData(LoginRequiredMixin, DatatablesServerSideView):

    model = post
    columns = ['id','title','email', 'start_date','end_date','create_date']
    searchable_columns = ['title','email']

    def get_initial_queryset(self):
        qs = super(docSearchListData, self).get_initial_queryset()
        return qs.filter(email__isnull=False)

class docSearchJsonData(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        data = ""
        id          = request.POST.get('id')
        rs          = get_object_or_404(post, id=id)
        json_data   = rs.json_data
        rep_data    = json_data.replace("'", "\"")
        data        = json.loads(rep_data)
            
        retrunMsg = {"data": data}
        return JsonResponse(retrunMsg)          