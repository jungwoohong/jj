from ast import Try
import json
from turtle import pos
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
import pandas as pd
from django.utils import timezone
from django.db.models import Subquery
from .forms import postForm, dataCollectionForm, shareUserForm, excelJsonDataForm
from .models import post, data_collection, share_user, excel_json_data
from datetime import datetime
from core.views import DatatablesServerSideView
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
from django.core import serializers
from background_task import background

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
                    
        arr = {"email": loginId, "title": title,"start_date":start_date,"end_date": end_date}            
        form = postForm(arr)

        if form.is_valid():
            if id == '':

                #post 저장
                record = form.save()
                jsonLoad = json.loads(json_data)

                # 데이터 셀 저장
                for idx,val in enumerate(jsonLoad):
                    excelTitle     = ''.join(list(val.keys()));
                    excelJsonData   = list(val.values());

                    arrJsonLoad = {"post": record.id, "title": excelTitle,"json_data":excelJsonData}
                    excelForm = excelJsonDataForm(arrJsonLoad) 
                    if excelForm.is_valid():
                        excelForm.save()

                    print(record.id)
                    self.dataCellSave(record.id,jsonLoad)

                msg = "저장하였습니다."                    
            else :
                #post 데이터 저장
                updateData = post.objects.get(id=id)
                updateData.title        = title
                updateData.start_date   = start_date
                updateData.end_date     = end_date
                updateData.save()

                # 엑셀데이터 저장
                jsonLoad = json.loads(json_data)

                updateDataExcelPostIds = excel_json_data.objects.filter(post=id)

                for idx, updateDataExcelPostId in enumerate(updateDataExcelPostIds) :
                    excelTitle     = ''.join(list(jsonLoad[idx].keys()))
                    excelJsonData   = list(jsonLoad[idx].values())

                    updateDataExcel             =  excel_json_data.objects.get(id=updateDataExcelPostId.id)
                    updateDataExcel.title       = excelTitle
                    updateDataExcel.json_data   = excelJsonData
                    updateDataExcel.save()

                msg = "수정하였습니다."                         

        retrunMsg = {"msg": msg, "form":form.errors}
        return JsonResponse(retrunMsg)

    @background(schedule=1)
    def dataCellSave(*args, **kwargs):
        print('=========================================================================')
        
        getId = args[0]
        data = args[1]
        print(getId)
        print('=========================================================================')
        print(data)
        print('=========================================================================')
        # data = excel_json_data.objects.filter(post=id)
        # print(data)
        


        #데이터 셀 저장
        # listexcelJsonData = list(excelJsonData)
        # cell_row = 0
        # cell_line = 0

        # for forData in listexcelJsonData[0] :
        #     cell_row = cell_row+1
        #     cell_line = 0
        #     for rs in forData :
                
        #         cell_line = cell_line+1
        #         cell_type = "cell"
        #         if cell_row == 1 or cell_row == 2 :
        #             cell_type = "header"

        #         arrDataCollection = {"post":id,"cell_row":cell_row,"cell_line":cell_line,"data":rs,"cell_type":cell_type} 
        #         formDataCollection = dataCollectionForm(arrDataCollection)

        #         if formDataCollection.is_valid():
                    
        #             #formDataCollection.save()            

        

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

        id          = request.POST.get('id')
        rss         = excel_json_data.objects.filter(post=id)
        data        = serializers.serialize("json", rss)
        data        = json.loads(data)

        retrunMsg = {"data": data}
        return JsonResponse(retrunMsg)            


class docSearchList(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'document/docSearchList.html')

class docSearchListData(LoginRequiredMixin, DatatablesServerSideView):

    model = post
    columns = ['id','title','email', 'start_date','end_date','create_date']
    searchable_columns = []

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():            
            return HttpResponseBadRequest()
        try:
            params = super(docSearchListData, self).read_parameters(request.GET)            
        except ValueError:
            return HttpResponseBadRequest()

        qs = self.get_initial_queryset(params)

        if len(params['orders']):            
            qs = qs.order_by(
                *[order.get_order_mode() for order in params['orders']])

        # super(docSearchListData, self).
        paginator = Paginator(qs, params['length'])
        return HttpResponse(
            json.dumps(
                self.get_response_dict(paginator, params['draw'],
                                       params['start']),
                cls=DjangoJSONEncoder
            ),
            content_type="application/json")

    def get_initial_queryset(self, *args, **kwargs):
        qs = None
        search_value = args[0].get('search_value')
        extra_search = args[0].get('extra_search')
        
        if (search_value != None) :
            dataCollectionRs = data_collection.objects.filter(data__contains=search_value)
            if(extra_search != None ) :
                if(extra_search != 'all' ) :
                    dataCollectionRs = dataCollectionRs.filter(cell_type=extra_search)

            qs = post.objects.filter(id__in=Subquery(dataCollectionRs.values('post')))

        else :
            qs = super(docSearchListData, self).get_initial_queryset()

        return qs         

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