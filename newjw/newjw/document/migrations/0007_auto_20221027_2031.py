# Generated by Django 3.2.15 on 2022-10-27 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0006_alter_post_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='memo',
            field=models.TextField(default='empty', null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(blank=True, default='empty', max_length=10, null=True),
        ),
    ]
