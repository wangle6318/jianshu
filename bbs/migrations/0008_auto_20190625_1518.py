# Generated by Django 2.2.1 on 2019-06-25 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0007_article_if_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=models.TextField(default='', verbose_name='文章'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(default='', max_length=300, verbose_name='标题'),
        ),
    ]
