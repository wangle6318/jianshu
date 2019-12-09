from django.db import models
from django.contrib.auth.models import User
from bbs.save import newStorage
# Create your models here.


class UserInfo(models.Model):
    sex_choice = (
        (u'1', u'男'),
        (u'2', u'女'),
        (u'3', u'保密'),
    )
    user = models.OneToOneField(User, verbose_name="用户", on_delete=models.CASCADE)
    name = models.CharField('昵称', max_length=30, unique=True)
    head_img = models.ImageField('头像', upload_to='head/%Y%m/', storage=newStorage(), default='head/head_img.jfif')
    phone = models.CharField('手机', max_length=11, null=True, blank=True)
    sex = models.CharField('性别', max_length=2, choices=sex_choice, default='3')
    intro = models.CharField('个人介绍', max_length=200, blank=True, null=True)
    wechatimg = models.ImageField('微信二维码', upload_to='wechat/%Y%m/', storage=newStorage(), null=True, blank=True)
    website = models.URLField('个人网站', null=True, blank=True)
    like = models.PositiveIntegerField('关注', default=0)
    fans = models.PositiveIntegerField('粉丝', default=0)
    article = models.PositiveIntegerField('文章', default=0)
    words = models.PositiveIntegerField('字数', default=0)
    loved = models.PositiveIntegerField('收获喜欢', default=0)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    # auto_now_add : 创建时间戳，不会被覆盖
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息管理'

    def __str__(self):
        return str(self.user_id)


class Article(models.Model):
    title = models.CharField('标题', max_length=300, default="")
    author = models.ForeignKey(User, verbose_name='作者', related_name="article_posts", on_delete=models.CASCADE)
    abstract = models.TextField('摘要', max_length=100, blank=True)
    have_img = models.ImageField('标题图', upload_to='titleimg/%Y%m/', null=True, blank=True)
    body = models.TextField('文章', default='')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    # auto_now_add : 创建时间戳，不会被覆盖
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    # auto_now: 自动将当前时间覆盖之前时间
    words = models.PositiveIntegerField('字数', default=0)
    views = models.PositiveIntegerField('阅读数', default=0)
    comments = models.PositiveIntegerField('评论量', default=0)
    love = models.PositiveIntegerField('喜欢数', default=0)
    collects = models.ManyToManyField(User, verbose_name='收藏', related_name='collect')
    loves = models.ManyToManyField(User, verbose_name='喜欢', related_name='love')
    if_publish = models.BooleanField('是否发布', default=False)


    class Meta:
        verbose_name = '文章管理'
        verbose_name_plural = '文章管理'
        ordering = ("-created_time",)

    def __str__(self):
        return self.title


class FriendShip(models.Model):
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('following', 'followed',)
        verbose_name = '关注'
        verbose_name_plural = '关注管理'

    def __str__(self):
        return str(self.id)


class Comments(models.Model):
    article = models.ForeignKey(Article, verbose_name='评论文章', related_name="post_comment", on_delete=models.CASCADE)
    content = models.TextField('评论内容')
    author = models.ForeignKey(User, verbose_name='作者', related_name="user_comment", on_delete=models.CASCADE)
    submit_date = models.DateTimeField('评论时间', auto_now_add=True)
    thumbsup = models.ManyToManyField(User, verbose_name='点赞', related_name='up')

    class Meta:
        verbose_name = '评论管理'
        verbose_name_plural = '评论管理'
        ordering = ("-submit_date",)

    def __self__(self):
        return '%s 评论了 %s' % (self.author.userinfo.name, self.article)


class CommentsReply(models.Model):
    article = models.ForeignKey(Article, verbose_name='回复文章', related_name="reply_article",on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, verbose_name='回复评论', related_name="reply_comment", blank=True, null=True, on_delete=models.CASCADE)
    content = models.TextField('回复内容')
    author_from = models.ForeignKey(User, verbose_name='作者', related_name="user_reply",on_delete=models.CASCADE)
    author_to = models.ForeignKey(User, verbose_name='回复给', related_name="reply_to",on_delete=models.CASCADE)
    submit_date = models.DateTimeField('评论时间', auto_now_add=True)
    thumbsup = models.ManyToManyField(User, verbose_name='点赞', related_name='reup')

    class Meta:
        verbose_name = '回复管理'
        verbose_name_plural = '回复管理'
        ordering = ("submit_date",)

    def __self__(self):
        return '%s @ %s ' % (self.author_from.userinfo.name, self.author_to.userinfo.name)
