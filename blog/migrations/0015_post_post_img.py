# Generated by Django 3.1.6 on 2021-03-15 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_projectmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_img',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]