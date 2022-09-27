from django.db import models

# 게시판 카테고리
class categories(models.Model):
    category_type = models.CharField(max_length=50)
    category_code = models.CharField(max_length=100)
    category_name = models.CharField(max_length=100)
    category_desc = models.CharField(max_length=100)
    list_count    = models.IntegerField(blank=True, null=True)
    authority     = models.IntegerField(blank=True, null=True)
    create_date   = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

# 게시물
class post(models.Model):
    category = models.ForeignKey(categories, on_delete=models.CASCADE)
    user_id  = models.CharField(max_length=100)
    title    = models.CharField(max_length=300)
    conent   = models.TextField()
    registered_date = models.DateTimeField(auto_now_add=True)
    last_update_date= models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(blank=True, default=0)

#댓글
class replies(models.Model):
    article   = models.ForeignKey(post, on_delete=models.CASCADE)
    user_id   = models.CharField(max_length=100)
    level     = models.IntegerField(blank=True, null=True)
    conent   = models.TextField()
    registered_date = models.DateTimeField(auto_now_add=True)
    last_update_date= models.DateTimeField(auto_now=True)

#첨부파일
class upload_file(models.Model):
    upload   = models.ForeignKey(post, on_delete=models.CASCADE)
    file_path   = models.CharField(max_length=100)
    file_name   = models.CharField(max_length=100)
    file_real_name   = models.CharField(max_length=100)
    file_ext   = models.CharField(max_length=100)
    file_size   = models.CharField(max_length=100)
    registered_date = models.DateTimeField(auto_now_add=True)
    last_update_date= models.DateTimeField(auto_now=True)       