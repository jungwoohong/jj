from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from datetime import date
from django.conf import settings
import json
import os
from core.views import DatatablesServerSideView
from django.core.files.storage import FileSystemStorage

from .forms import *
from .models import post
from .models import upload_file
import mimetypes

class index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'board/boardList.html')


class getBoardListData(LoginRequiredMixin, DatatablesServerSideView):

    model = post
    columns = ['id', 'title', 'user_id', 'registered_date', 'view_count']
    searchable_columns = ['title']
    #foreign_fields = {'create': 'create__date'}

    def get_initial_queryset(self):
        qs = super(getBoardListData, self).get_initial_queryset()
        return qs.filter(id__isnull=False)


class postReg(LoginRequiredMixin, View):
    def get(self, request):

        context = {}
        id = request.GET.get('id')
        if(id) :       
            data = get_object_or_404(post, id=id)
            fileRs = upload_file.objects.filter(upload=id)

            if data.user_id != request.user.username:                
                raise Http404("권한이 없습니다.")
                
            context = {
                "data":data,
                "fileRs":fileRs
            }
                
        return render(request, 'board/reg.html', context)


class postSave(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        msg = "실패하였습니다."

        folder_name = str(date.today().strftime("%Y%m%d"))
        MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)
        path = os.path.join(MEDIA_ROOT, folder_name)

        if not os.path.isdir(path):
            os.makedirs(path)

        id = request.POST.get('id')
        category = request.POST.get('category')
        title = request.POST.get('title')
        content = request.POST.get('content')
        loginId = request.user.username
        returnId = None

        arr = {"user_id": loginId, "category": category, "title": title, "content": content}
        form = postForm(arr)
        
        if form.is_valid():
            if id == '':
                record = form.save()
                returnId = record.id
                try:
                    for myfile in request.FILES.getlist('attachFile'):   

                        fileArr = {"upload": record.id,
                                    "file_path": path, 
                                    "file_name": myfile.name, 
                                    "file_real_name": myfile.name,
                                    "file_ext": os.path.splitext(myfile.name)[-1].replace(".", ""), 
                                    "file_size": myfile.size}

                        fileForm = uploadFileForm(fileArr)
                        if fileForm.is_valid():
                          
                            fs = FileSystemStorage(location=path)
                            fs.save(myfile.name, myfile)

                            fileForm.save()  

                except MultiValueDictKeyError:
                    myfile = False                         

                msg = "저장하였습니다."

            else:
                updateData = post.objects.get(id=id)
                updateData.title = title
                updateData.content = content
                updateData.save()
                try:
                    
                    for myfile in request.FILES.getlist('attachFile'):                   
                        fileArr = {"upload": id,
                                    "file_path": path, 
                                    "file_name": myfile.name, 
                                    "file_real_name": myfile.name,
                                    "file_ext": os.path.splitext(myfile.name)[-1].replace(".", ""), 
                                    "file_size": myfile.size}

                        fileForm = uploadFileForm(fileArr)
                        if fileForm.is_valid():                          
                            fs = FileSystemStorage(location=path)
                            fs.save(myfile.name, myfile)

                            fileForm.save()  

                except MultiValueDictKeyError:
                    myfile = False

                returnId = id
                msg = "수정하였습니다."

        retrunMsg = {"msg": msg, "form":form.errors, "returnId":returnId}

        return JsonResponse(retrunMsg)


class postDetailView(LoginRequiredMixin, View):
    def get(self, request):

        id = request.GET.get('id')
        if id != '':
            try:
                rs = post.objects.get(id=id)
                fileRs = upload_file.objects.filter(upload=id)
                context = {
                    'rs': rs,
                    'fileRs':fileRs
                }
                return render(request, 'board/detail.html', context)
            except post.DoesNotExist:
                return


        return render(request, 'board/boardList.html')

class fileDownload(LoginRequiredMixin, View):
    def get(self, request,id):
     
        rs = upload_file.objects.get(id=id)

        filename = rs.file_name
        filepath = os.path.join(rs.file_path, filename)
        mime_type, _ = mimetypes.guess_type(filepath)
        
        fs = FileSystemStorage(rs.file_path)
        response = FileResponse(fs.open(filepath, 'rb'),content_type=mime_type)

        response['Content-Disposition'] = 'attachment; filename='+filename                            

        return response

class fileDelete(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        result = ""
        id = request.POST.get('id')

        try:
            upload_file.objects.filter(id=id).delete()
            result = 1
        except Exception():
            result = 0
     
        returnVal = { 'result': result }

        return JsonResponse(returnVal)