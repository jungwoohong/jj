# Generated by Django 3.2.15 on 2022-11-01 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0009_alter_post_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='excel_json_data',
            name='style_data',
            field=models.TextField(default='empty', null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='memo',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
