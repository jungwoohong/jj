import json
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from newjw.document.models import post as doc_post
from newjw.sharedoc.models import post as share_post
from django.core import serializers

class scheduleChk(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        start       = request.POST.get('start')
        end         = request.POST.get('end')
        loginId     = request.user.username

        doc_post_rss      = doc_post.objects.filter(email=loginId, start_date__range=(start, end))
        doc_data          = serializers.serialize("json", doc_post_rss)
        doc_data          = json.loads(doc_data)
        share_post_rss    = share_post.objects.filter(email=loginId, start_date__range=(start, end))
        share_data        = serializers.serialize("json", share_post_rss)
        share_data        = json.loads(share_data)

        retrunMsg = {
                     "doc_data" : doc_data,
                     "share_data" : share_data
                    }

        return JsonResponse(retrunMsg)      