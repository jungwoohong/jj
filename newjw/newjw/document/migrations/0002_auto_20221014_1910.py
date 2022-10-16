# Generated by Django 3.2.15 on 2022-10-14 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='json_data',
        ),
        migrations.CreateModel(
            name='excel_json_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_data', models.TextField(default='empty', null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.post')),
            ],
            options={
                'db_table': 'doc_excel_json_data',
            },
        ),
    ]
