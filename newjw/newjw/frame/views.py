from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json

#from .models import *


class frameViewReg(LoginRequiredMixin, View):
    
    def get(self, request):
       
        return render(request, 'frame/reg.html')


class frameViewSave(LoginRequiredMixin, View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(frameViewSave, self).dispatch(request, *args, **kwargs)

    def post(self,request,*args, **kwargs):
        data = json.loads(request.body)
        # post = posta()
        # post.email = "a"
        # post.json_data = data

        
        return JsonResponse({"key": "value"})
