# Generated by Django 3.2.15 on 2022-10-27 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharedoc', '0003_auto_20221023_1236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='post',
            name='memo',
            field=models.TextField(default='empty', null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(blank=True, default='R', max_length=10, null=True),
        ),
    ]
