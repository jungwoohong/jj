# Generated by Django 3.2.15 on 2022-10-18 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0003_excel_json_data_title'),
    ]

    operations = [
        migrations.DeleteModel(
            name='share_user',
        ),
    ]
