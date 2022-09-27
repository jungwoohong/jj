from django.db import models

# 템플릿 저장소
class post(models.Model):
    title   = models.CharField(max_length=300)
    key = models.CharField(max_length=100)
    create_date   = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)