# Generated by Django 2.2.1 on 2019-06-14 02:04

import bbs.save
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0002_auto_20190614_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='head_img',
            field=models.ImageField(default='head/head_img.jfif', storage=bbs.save.newStorage(), upload_to='head/%Y%m/', verbose_name='头像'),
        ),
    ]
