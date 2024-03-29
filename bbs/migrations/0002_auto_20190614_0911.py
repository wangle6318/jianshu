# Generated by Django 2.2.1 on 2019-06-14 01:11

import bbs.save
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='手机'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='wechatimg',
            field=models.ImageField(blank=True, null=True, storage=bbs.save.newStorage(), unique=True, upload_to='wechat/%Y%m/', verbose_name='微信二维码'),
        ),
    ]
