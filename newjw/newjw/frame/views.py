from django.core.mail import EmailMessage
from pprint import pprint
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponse, JsonResponse
from sqlalchemy import null
from core.views import DatatablesServerSideView
from django.core import serializers

import json
from .models import post
from .forms import postForm



class frameViewReg(LoginRequiredMixin, View):

    def get(self, request):
        
        context = {}
        id = request.GET.get('id')
        
        if(id) :       
                data = get_object_or_404(post, id=id)
                context = {"data":data}
                
        return render(request, 'frame/reg.html',context)


class frameViewSave(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        msg = "실패하였습니다."

        id          = request.POST.get('id')
        title       = request.POST.get('title')
        json_data   = request.POST.get('data')
        style_data  = request.POST.get('style_data')
        loginId     = request.user.username            
                    
        arr = {"email": loginId,"json_data": json_data, "title": title, "style_data":style_data }            
        form = postForm(arr)

        if form.is_valid():
            if id == '':
                record = form.save()
                msg = "저장하였습니다."                    
            else :
                updateData = post.objects.get(id=id)
                updateData.json_data    = json_data
                updateData.title        = title
                updateData.style_data   = style_data
                updateData.save()
                msg = "수정하였습니다."                         

        retrunMsg = {"msg": msg}
        return JsonResponse(retrunMsg)


class frameLoadList(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'frame/frameList.html')


class frameLoadListData(LoginRequiredMixin, DatatablesServerSideView):

    model = post
    columns = ['id','title','email', 'create_date']
    searchable_columns = ['title','email']

    def get_initial_queryset(self):
        loginId     = self.request.user.username
        qs = super(frameLoadListData, self).get_initial_queryset()
        return qs.filter(email=loginId)    
    
class frameJsonData(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        data = null
        
        if request.method == 'POST':
            id          = request.POST.get('id')
            rss         = post.objects.filter(id=id)
            data        = serializers.serialize("json", rss)
            data        = json.loads(data)  

        retrunMsg = {"data": data}
        return JsonResponse(retrunMsg)    

class docToSearchList(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'frame/docToSearchList.html')


class docToSearchListData(LoginRequiredMixin, DatatablesServerSideView):

    model = post
    columns = ['id','title','email', 'create_date']
    searchable_columns = ['title','email']