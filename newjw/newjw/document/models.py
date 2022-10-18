from django.db import models

# 문서 보관함
class post(models.Model):
    email               = models.CharField(max_length=50)
    title               = models.CharField(max_length=200)
    start_date          = models.DateTimeField()
    end_date            = models.DateTimeField()
    create_date         = models.DateTimeField(auto_now_add=True)
    last_update_date    = models.DateTimeField(auto_now=True)

    class Meta : 
         db_table = 'doc_post'

# 데이터 보관함
class data_collection(models.Model):
    post                = models.ForeignKey(post, on_delete=models.CASCADE)
    cell_row            = models.IntegerField(blank=True, null=True)
    cell_line           = models.IntegerField(blank=True, null=True)  
    data                = models.CharField(max_length=300)
    cell_type           = models.CharField(max_length=10)
    create_date         = models.DateTimeField(auto_now_add=True)
    last_update_date    = models.DateTimeField(auto_now=True)   

    class Meta : 
         db_table = 'doc_data_collection'


# 엑셀시트 저장
class excel_json_data(models.Model):
    post                = models.ForeignKey(post, on_delete=models.CASCADE)
    title               = models.CharField(max_length=200,null=True,default='empty')
    json_data           = models.TextField(null=True,default='empty')

    class Meta : 
         db_table = 'doc_excel_json_data'         
