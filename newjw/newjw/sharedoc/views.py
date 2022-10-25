from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import Http404, JsonResponse
from django.core import serializers
from django.db.models import Subquery
from core.views import DatatablesServerSideView
from django.db.models import Q
from .models import *
from .forms import *
from newjw.document.models import post as doc_post
# from newjw.sharedoc.models import *
import json
from django.core.paginator import Paginator
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.core.serializers.json import DjangoJSONEncoder
from newjw.document.share import shareDataCellSave


class selectUserList(LoginRequiredMixin, View):

    def get(self, request):

        return render(request, 'sharedoc/selectUserList.html')


class selectUserListData(LoginRequiredMixin, View):

    def get(self, request):

        id = request.GET.get('id')
        context = {}

        groupset = group_test_table.objects.all()
        group = serializers.serialize("json", groupset)
        group = json.loads(group)

        userset = user_test_table.objects.all()
        user = serializers.serialize("json", userset)
        user = json.loads(user)

        context = {
            "group": group,
            "user": user
        }
        # a = user_test_table.objects.select_related('dept_code')
        # print(a.dept_code.dept_name)
        return JsonResponse(context)


class myWriteList(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'sharedoc/docList.html')


class myWriteListData(LoginRequiredMixin, DatatablesServerSideView):

    model = post
    columns = ['id', 'title', 'email', 'start_date', 'end_date', 'status']
    searchable_columns = ['title']

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        try:
            params = super(myWriteListData, self).read_parameters(request.GET)
        except ValueError:
            return HttpResponseBadRequest()

        loginId = request.user.username
        qs = self.get_initial_queryset(loginId)

        if 'search_value' in params:
            qs = super(myWriteListData, self).filter_queryset(params['search_value'], qs)

        if len(params['orders']):
            qs = qs.order_by(
                *[order.get_order_mode() for order in params['orders']])

        paginator = Paginator(qs, params['length'])
        return HttpResponse(
            json.dumps(
                super(myWriteListData, self).get_response_dict(paginator, params['draw'],
                                                               params['start']),
                cls=DjangoJSONEncoder
            ),
            content_type="application/json")

    def get_initial_queryset(self, *args, **kwargs):
        qs = None
        loginId = args[0]
        docPostRs = doc_post.objects.filter(status='I')  # Original Document ing
        qs = post.objects.filter(doc_post__in=Subquery(docPostRs.values('id')))
        qs = qs.filter(Q(email=loginId))

        return qs


class shareDocDetail(LoginRequiredMixin, View):

    def get(self, request):

        context = {}
        id = request.GET.get('id')

        if(id):
            data = get_object_or_404(post, id=id)
            context = {"data": data}

        return render(request, 'sharedoc/reg.html', context)


class shareDocSave(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        msg = "실패하였습니다."

        id = request.POST.get('id')
        json_data = request.POST.get('json_data')
        title = request.POST.get('title')
        loginId = request.user.username

        arr = {"email": loginId, "title": title}
        form = sharePostForm(arr)

        if form.is_valid():

            # post 데이터 저장
            updateData = post.objects.get(id=id)
            updateData.title = title
            updateData.save()

            # 데이터 셀 저장
            jsonLoad = json.loads(json_data)
            # 해당 데이터 삭제
            excel_json_data.objects.filter(post=id).delete()

            for idx, val in enumerate(jsonLoad):
                excelTitle = ''.join(list(val.keys()))
                excelJsonData = list(val.values())

                arrJsonLoad = {"post": id, "title": excelTitle, "json_data": excelJsonData}
                excelForm = shareExcelJsonDataForm(arrJsonLoad)
                if excelForm.is_valid():
                    excelForm.save()

            # 해당 데이터 삭제
            data_collection.objects.filter(post=id).delete()
            shareDataCellSave(id, excelJsonData)

            msg = "저장하였습니다."

        retrunMsg = {"msg": msg, "form": form.errors}
        return JsonResponse(retrunMsg)
