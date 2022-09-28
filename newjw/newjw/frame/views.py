from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class frameViewReg(LoginRequiredMixin, View):
    
    def get(self, request):
        return render(request, 'frame/reg.html')

    def post(self, request):
        return render(request, 'frame/reg.html')  