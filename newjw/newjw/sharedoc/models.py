from django.db import models
from newjw.document.models import post as doc_post

# 공유 문서 보관함
class post(models.Model):
    doc_post            = models.ForeignKey(doc_post, on_delete=models.CASCADE)
    email               = models.CharField(max_length=50)
    title               = models.CharField(max_length=200)
    start_date          = models.DateTimeField()
    end_date            = models.DateTimeField()
    create_date         = models.DateTimeField(auto_now_add=True)
    last_update_date    = models.DateTimeField(auto_now=True)
    status              = models.CharField(max_length=10,blank=True, null=True, default='R')


# 공유자
class user(models.Model):
    post                = models.ForeignKey(post, on_delete=models.CASCADE)
    doc_post            = models.ForeignKey(doc_post, on_delete=models.CASCADE)
    email               = models.CharField(max_length=50)   

# 데이터 보관함
class data_collection(models.Model):
    post                = models.ForeignKey(post, on_delete=models.CASCADE)
    cell_row            = models.IntegerField(blank=True, null=True)
    cell_line           = models.IntegerField(blank=True, null=True)  
    data                = models.CharField(max_length=300)
    cell_type           = models.CharField(max_length=10)
    create_date         = models.DateTimeField(auto_now_add=True)
    last_update_date    = models.DateTimeField(auto_now=True)   

# 공유 엑셀시트 저장
class excel_json_data(models.Model):
    post                = models.ForeignKey(post, on_delete=models.CASCADE)
    title               = models.CharField(max_length=200,null=True,default='empty')
    json_data           = models.TextField(null=True,default='empty')

class group_test_table(models.Model):
    dept_code           = models.CharField(max_length=150 ,null=True)
    dept_name           = models.CharField(max_length=150 ,null=True)
    parent_code         = models.CharField(max_length=150 ,null=True)
    depth               = models.CharField(max_length=50)   

class user_test_table(models.Model):
    email               = models.CharField(max_length=50)   
    dept_code            = models.ForeignKey('group_test_table', on_delete=models.SET_NULL, null=True , db_column='dept_code')

