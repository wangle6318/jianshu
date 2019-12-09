# Generated by Django 2.2.1 on 2019-09-04 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bbs', '0011_auto_20190731_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('submit_date', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('artid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comment', to='bbs.Article', verbose_name='评论文章')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '评论管理',
                'verbose_name_plural': '评论管理',
                'ordering': ('-submit_date',),
            },
        ),
        migrations.CreateModel(
            name='CommentsReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='回复内容')),
                ('submit_date', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('art_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_article', to='bbs.Article', verbose_name='回复文章')),
                ('author_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reply', to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('author_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_to', to=settings.AUTH_USER_MODEL, verbose_name='回复给')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_comment', to='bbs.Comments', verbose_name='回复评论')),
            ],
            options={
                'verbose_name': '回复管理',
                'verbose_name_plural': '回复管理',
                'ordering': ('submit_date',),
            },
        ),
    ]