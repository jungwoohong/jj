# Generated by Django 3.2.15 on 2022-10-27 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frame', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='', max_length=300, null=True),
        ),
    ]
