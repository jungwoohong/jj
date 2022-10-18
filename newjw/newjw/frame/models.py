from django.db import models

# 템플릿 저장소
class post(models.Model):
    email               = models.CharField(max_length=150 ,null=True,default='')
    title              = models.CharField(max_length=300 ,null=True,default='')
    json_data           = models.TextField(null=True,default='')
    create_date         = models.DateTimeField(auto_now_add=True)
    last_update_date    = models.DateTimeField(auto_now=True)
    
    class Meta : 
         ordering = ['-id']
              
    #     abstract = True

# 엑셀 데이터
class post_data(models.Model):
    post_id             = models.IntegerField(blank=True, null=True)
    row                 = models.IntegerField(blank=True, null=True)
    data                = models.CharField(max_length=300)
    create_date         = models.DateTimeField(auto_now_add=True)
    last_update_date    = models.DateTimeField(auto_now=True)     