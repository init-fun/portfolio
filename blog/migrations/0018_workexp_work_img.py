# Generated by Django 3.1.6 on 2021-03-15 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_post_post_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='workexp',
            name='work_img',
            field=models.ImageField(default=1, upload_to='work_images/'),
            preserve_default=False,
        ),
    ]
