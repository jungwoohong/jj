from ast import Try
import json
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import pandas as pd
from django.utils import timezone
from django.db.models import Subquery
from .forms import postForm, dataCollectionForm, excelJsonDataForm
from .models import post, data_collection, excel_json_data
from datetime import datetime
from core.views import DatatablesServerSideView
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
from django.core import serializers
from .task import dataCellSave
from .share import sharePostSave, shareExcelJsonDataSave, shareDataCellSave
from newjw.sharedoc.models import post as share_post, excel_json_data as share_excel_json_data
from django.core.mail import EmailMessage

class docReg(LoginRequiredMixin, View):

    def get(self, request):

        context = {}
        id = request.GET.get('id')

        if(id):
             data = get_object_or_404(post, id=id)
             shareUsers = share_post.objects.filter(doc_post=id).values('email')
             shareRs = []
             
             for shareUser in shareUsers :
                shareRs.append(shareUser['email'])

             context = {"data":data,"shareUser":','.join(shareRs)}

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
        memo        = request.POST.get('memo')
        status      = request.POST.get('status')
        statusAct   = status
        loginId     = request.user.username
        start_date  = datetime.strptime(request.POST.get('start_date'), "%Y.%m.%d")
        start_date  = timezone.make_aware(start_date)
        end_date    = datetime.strptime(request.POST.get('end_date'), "%Y.%m.%d")
        end_date    = timezone.make_aware(end_date)
        share_user  = request.POST.get('shareUser')
        share_user_list = share_user.split(',')
        share_post_list = []

        if(status == 'B') : 
            status= 'P'
          
        arr = {"email": loginId, "title": title,"start_date":start_date,"end_date": end_date,"memo":memo,"status":status}           
        form = postForm(arr)

        if form.is_valid():
            if id == '':

                #post 저장
                record = form.save()
                jsonLoad = json.loads(json_data)

                
                # sharedoc post에 값 저장
                for user in share_user_list:
                    share_arr = {"doc_post" : record.id, "email": user, "title": title,"start_date":start_date,"end_date": end_date}
                    share_post_id = sharePostSave(share_arr)
                    share_post_list.append(share_post_id)                    
            
                # 데이터 셀 저장
                for idx,val in enumerate(jsonLoad):
                    excelTitle     = ''.join(list(val.keys()))
                    excelJsonData   = list(val.values())

                    arrJsonLoad = {"post": record.id, "title": excelTitle,"json_data":excelJsonData}
                    excelForm = excelJsonDataForm(arrJsonLoad) 
                    if excelForm.is_valid():
                        excelForm.save()

                    dataCellSave(record.id,excelJsonData)

                    for share_id in share_post_list:
                        shareArrJsonLoad = {"post": share_id, "title": excelTitle, "json_data":excelJsonData}
                        shareExcelJsonDataSave(shareArrJsonLoad)
                        shareDataCellSave(share_id,excelJsonData)
                    
                email_title = ''
                email_body  = ''

                # email = EmailMessage(email_title,email_body,to=share_user_list)  
                # email.send()
                msg = "저장하였습니다."    

            else :
                #post 데이터 저장
                updateData = post.objects.get(id=id)
                updateData.title        = title
                updateData.start_date   = start_date
                updateData.end_date     = end_date
                updateData.memo         = memo
                updateData.status       = status
                updateData.save()

                
                # 데이터 셀 저장
                jsonLoad = json.loads(json_data)
                # 해당 데이터 삭제
                excel_json_data.objects.filter(post=id).delete()
                
                for idx,val in enumerate(jsonLoad):
                    excelTitle     = ''.join(list(val.keys()))
                    excelJsonData   = list(val.values())

                    arrJsonLoad = {"post": id, "title": excelTitle,"json_data":excelJsonData}
                    excelForm = excelJsonDataForm(arrJsonLoad) 
                    if excelForm.is_valid():
                        excelForm.save()

                if(statusAct=='B') : 
                    share_post.objects.filter(doc_post=id).delete()

                    for user in share_user_list:
                        share_arr = {"doc_post" : id, "email": user, "title": title,"start_date":start_date,"end_date": end_date}
                        share_post_id = sharePostSave(share_arr)
                        share_post_list.append(share_post_id)



                    for share_id in share_post_list:
                        shareArrJsonLoad = {"post": share_id, "title": excelTitle, "json_data":excelJsonData}
                        shareExcelJsonDataSave(shareArrJsonLoad)
                        shareDataCellSave(share_id,excelJsonData)                 

                email_title = ''
                email_body  = ''

                # email = EmailMessage(email_title,email_body,to=share_user_list)  
                # email.send()
                msg = "수정하였습니다."                         

        retrunMsg = {"msg": msg, "form":form.errors}
        return JsonResponse(retrunMsg)      


class docLoadList(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'document/docList.html')

class docLoadListData(LoginRequiredMixin, DatatablesServerSideView):

    model = post
    columns = ['id','title','email', 'start_date','end_date','create_date','status']
    searchable_columns = ['title','email']

    def get_initial_queryset(self):
        loginId     = self.request.user.username
        qs = super(docLoadListData, self).get_initial_queryset()
        qs.filter(email=loginId)
        return qs.filter(email=loginId)

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

class docDelete(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        data    = ""
        id      = request.POST.get('id')
        rs = post.objects.get(id=id)
        rs.delete()
            
        retrunMsg = {"data": data}
        return JsonResponse(retrunMsg)

class shareDocCheck(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        data    = ""
        id      = request.POST.get('id')
        rs      = share_post.objects.filter(doc_post=id).exclude(status='R')
        data    = serializers.serialize("json", rs)
        data    = json.loads(data)

        retrunMsg = {"data": data}
        return JsonResponse(retrunMsg)        


class shareUserList(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'document/shareUserList.html')

class shareUserListData(LoginRequiredMixin, DatatablesServerSideView):

    model = share_post
    columns = ['id','title','email','status','last_update_date','memo']
    searchable_columns = []

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():            
            return HttpResponseBadRequest()
        try:
            params = super(shareUserListData, self).read_parameters(request.GET)            
        except ValueError:
            return HttpResponseBadRequest()

        qs = self.get_initial_queryset(params)

        if len(params['orders']):            
            qs = qs.order_by(
                *[order.get_order_mode() for order in params['orders']])

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
        extra_search = args[0].get('extra_search')

        qs = super(shareUserListData, self).get_initial_queryset()
        return qs.filter(doc_post=extra_search)

class shareJsonData(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        id          = request.POST.get('id')
        rss         = share_excel_json_data.objects.filter(post=id)
        data        = serializers.serialize("json", rss)
        data        = json.loads(data)

        retrunMsg = {"data": data}
        return JsonResponse(retrunMsg)