# Generated by Django 3.2.15 on 2022-10-18 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0004_delete_share_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(max_length=10, null=True),
        ),
    ]