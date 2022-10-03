from pprint import pprint
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin

class docReg(LoginRequiredMixin, View):

    def get(self, request):
        
        context = {}
        id = request.GET.get('id')
        
        if(id) :       
                # data = get_object_or_404(post, id=id)
                # context = {"data":data}
                print('')
                
        return render(request, 'document/reg.html',context)
    
class docUpload(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'document/upload.html')
    
    def post(self, request):
        
        file = request.FILES['file1']
        print(file)
        return render(request, 'document/upload.html')    