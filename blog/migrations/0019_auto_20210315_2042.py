# Generated by Django 3.1.6 on 2021-03-15 15:12

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_workexp_work_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(default=blog.models.anon_username, max_length=10),
        ),
    ]
