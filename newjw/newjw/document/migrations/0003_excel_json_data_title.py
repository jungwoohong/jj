# Generated by Django 3.2.15 on 2022-10-17 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_auto_20221014_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='excel_json_data',
            name='title',
            field=models.CharField(default='empty', max_length=200, null=True),
        ),
    ]