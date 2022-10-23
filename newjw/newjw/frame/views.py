from pprint import pprint
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import Http404, JsonResponse
from sqlalchemy import null
from core.views import DatatablesServerSideView
from newjw.libs.mail import mailSend

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

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(frameViewSave, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        msg = "실패하였습니다."

        id          = request.POST.get('id')
        json_data   = request.POST.get('data')
        title       = request.POST.get('title')
        loginId     = request.user.username            
                    
        arr = {"email": loginId,"json_data": json_data, "title": title }            
        form = postForm(arr)

        if form.is_valid():
            if id == '':
                record = form.save()
                msg = "저장하였습니다."                    
            else :
                updateData = post.objects.get(id=id)
                updateData.json_data    = json_data
                updateData.title        = title
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
    
class frameJsonData(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        data = null
        
        if request.method == 'POST':
            id          = request.POST.get('id')
            rs          = get_object_or_404(post, id=id)
            json_data   = rs.json_data
            rep_data    = json_data.replace("'", "\"")
            data        = json.loads(rep_data)
            
        retrunMsg = {"data": data}
        return JsonResponse(retrunMsg)    

class docToSearchList(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'frame/docToSearchList.html')


class docToSearchListData(LoginRequiredMixin, DatatablesServerSideView):

    model = post
    columns = ['id','title','email', 'create_date']
    searchable_columns = ['title','email']

class mailtest(LoginRequiredMixin, View):

    def get(self, request):
        frm ="jungwoo02@gmail.com"
        to = "eunju9832@naver.com"
        subject = "테스트입니다."
        content = "테스트입니다."
        mailSend(frm,to,subject,content)

        retrunMsg = {"data": "abc"}
        return JsonResponse(retrunMsg)                