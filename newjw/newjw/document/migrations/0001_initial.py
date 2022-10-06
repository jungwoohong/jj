# Generated by Django 3.2.15 on 2022-10-06 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('json_data', models.TextField(default='empty', null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'doc_post',
            },
        ),
        migrations.CreateModel(
            name='share_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.post')),
            ],
            options={
                'db_table': 'doc_share_user',
            },
        ),
        migrations.CreateModel(
            name='data_collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cell_row', models.IntegerField(blank=True, null=True)),
                ('cell_line', models.IntegerField(blank=True, null=True)),
                ('data', models.CharField(max_length=300)),
                ('cell_type', models.CharField(max_length=10)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_update_date', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.post')),
            ],
            options={
                'db_table': 'doc_data_collection',
            },
        ),
    ]
