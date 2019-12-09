from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from bbs.models import UserInfo, Article, FriendShip, Comments, CommentsReply
from django.contrib.auth.models import User
from bbs.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from json import dumps
from django.http import QueryDict
from django.utils.html import strip_tags
from bbs.image import get_img_url, save_img, crop_img
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import os
import random
import time
from jianshu.settings import EMAIL_HOST_USER
import bbs.signals
# Create your views here.


def index(request):
    user = request.user
    if user.is_anonymous:
        user_info = UserInfo()
        recommend_author = UserInfo.objects.all().order_by('-words', '-fans', '-loved')[:5]
    else:
        user_info = UserInfo.objects.get(user_id=user.id)
        recommend_author = UserInfo.objects.all().exclude(user__followed__following=user).order_by('-words', '-fans', '-loved')[:5]
    article = Article.objects.filter(if_publish=True).order_by('-last_modified_time')[:6]
    for author in recommend_author:
        if author.words > 999:
            author.words = str(round(author.words/1000, 1)) + 'k'
        else:
            author.words = str(author.words)
        if author.loved > 999:
            author.loved = str(round(author.loved/1000, 1)) + 'k'
        else:
            author.loved = str(author.loved)
    content = {
        "user": user,
        "user_info": user_info,
        "article": article,
        "rec_author": recommend_author
    }
    return render(request, 'bbs/index.html', content)


def signup(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.method == 'GET':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        request.session.set_expiry(0)
        login_form = LoginForm()
        return render(request, 'bbs/signup.html', {"login_form": login_form})
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            username = cd['acct']
            password = cd['password']
            remember = cd['remember']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(7*24*3600)
                else:
                    request.session.set_expiry(0)
                if 'signin' in request.session['login_from']:
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect(request.session['login_from'])
            else:
                return render(request, 'bbs/signup.html', {"login_form": login_form, "error": "用户名或密码错误"})


class jianshuBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            try:
                phone_id = UserInfo.objects.get(phone=username).user_id
            except UserInfo.DoesNotExist:
                phone_id = 0
            user = User.objects.get(Q(username=username) | Q(email=username) | Q(id=phone_id))
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception as e:  # 可以捕获除与程序退出sys.exit()相关之外的所有异常
            print(e)
            return None


def signin(request):
    """
    注册
    :param request:
    :return:
    """

    if request.method == 'GET':
        register = RegisterForm()
        return render(request, 'bbs/signin.html', {"reg_form": register})
    elif request.method == 'POST':
        register = RegisterForm(request.POST)
        if register.is_valid():
            cd = register.cleaned_data
            username = cd['acct']
            password = cd['password']
            name = cd['name']
            # 事务回滚,create同时成功才入库
            with transaction.atomic():
                new_user = User.objects.create_user(username=username, password=password)
                UserInfo.objects.create(user=new_user, name=name)
            return HttpResponseRedirect('signup')
        return render(request, 'bbs/signin.html', {"reg_form": register, "error": "注册失败,请重试"})


def signout(request):
    logout(request)
    return HttpResponseRedirect('/')


def get_img_path(parent):
    current_time = time.localtime()
    year = str(current_time.tm_year)
    month = str(current_time.tm_mon)
    img_path = parent + '\\' + year + '\\' + month + '\\'
    path = os.path.join(settings.MEDIA_ROOT, img_path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


@login_required(login_url='bbs/../signup')
def publish_article(request):
    if request.method == 'GET':
        art = Article.objects.filter(Q(author=request.user) & Q(if_publish=False)).values('id', 'title', 'body',
                                    'last_modified_time').order_by('-last_modified_time')
        user_info = UserInfo.objects.get(user_id=request.user.id)
        content = {
            "article": art,
            "userinfo": user_info
        }
        return render(request, 'bbs/write.html', content)
    elif request.method == 'POST':
        article_id = request.POST.get('id')
        title = request.POST.get('title')
        body = request.POST.get('body')
        word = strip_tags(body).strip().replace("&nbsp;", "").replace(" ", "")
        abstract = word[:70]+"……"
        img_urls = get_img_url(body)
        title_img = ''
        if img_urls:
            for url in img_urls:
                img_path = save_img(url, get_img_path("titleimg"))
                if img_path:
                    crop_img(2/3, img_path)
                    title_img = img_path.split("media\\")[-1]
                    break
        words = len(word)
        user = UserInfo.objects.get(user=request.user)
        if article_id.isdigit():
            with transaction.atomic():
                user.words += words
                user.article += 1
                user.save()
                article = Article.objects.get(id=article_id)
                article.title = title
                article.abstract = abstract
                article.body = body
                article.words = words
                article.if_publish = True
                if title_img:
                    article.have_img = title_img
                article.save()
        else:
            with transaction.atomic():
                if title_img:
                    article = Article.objects.create(title=title, abstract=abstract, body=body, have_img=title_img,
                                                     words=words, if_publish=True, author=request.user)
                else:
                    article = Article.objects.create(title=title, abstract=abstract, body=body, words=words,
                                                     if_publish=True, author=request.user)
                user.words += words
                user.article += 1
                user.save()
        content = {
            "article_id": article.id
        }
        return HttpResponse(dumps(content))


def save_article(request):
    if request.method == 'POST':
        virtual_id = request.POST.get('id')
        title = request.POST.get('title')
        body = request.POST.get('body')
        article_id = ''
        if virtual_id.isdigit():
            article = Article.objects.get(id=int(virtual_id))
            article.title = title
            article.body = body
            article.save()
        else:
            article = Article.objects.create(title=title, body=body, author=request.user)
            article_id = str(article.id)
        content = {
            'virtual_id': virtual_id,
            'article_id': article_id
        }
        return HttpResponse(dumps(content))


def get_article(request):
    if request.method == 'POST':
        body = Article.objects.get(id=request.POST.get('id')).body
        content = {
            "body": body
        }
        return HttpResponse(dumps(content))


def del_article(request):
    delete = QueryDict(request.body)
    article_id = delete.get('id')
    Article.objects.get(id=article_id).delete()
    content = {
        "status": "success"
    }
    return HttpResponse(dumps(content))


def article_page(request, article_id):
    if request.method == 'GET':
        try:
            user_info = UserInfo.objects.get(user_id=request.user.id)
        except UserInfo.DoesNotExist:
            user_info = UserInfo()
        article = Article.objects.get(Q(id=article_id) & Q(if_publish=True))
        article.views += 1
        article.save(update_fields=['views'])
        is_collect = False
        if article.collects.filter(id=request.user.id):
            is_collect = True
        is_love = False
        if article.loves.filter(id=request.user.id):
            is_love = True
        is_follow = False
        if not request.user.is_anonymous:
            if FriendShip.objects.filter(following=request.user, followed=article.author):
                is_follow = True
        comments = Comments.objects.filter(article=article)
        replys = CommentsReply.objects.filter(article=article)
        content = {
            "user_info": user_info,
            "article": article,
            "collect": is_collect,
            "love": is_love,
            "follow": is_follow,
            "comments": comments,
            "replys": replys
        }
        return render(request, 'bbs/article.html', content)


def load_more_article(request):
    if request.method == 'GET':
        offset = int(request.GET.get("offset"))
        articles = Article.objects.filter(if_publish=True).order_by('-last_modified_time')[offset * 6:(offset + 1) * 6]
        article_list = []
        if_have = False
        for article in articles:
            dic = {}
            dic['id'] = article.id
            dic['title'] = article.title
            dic['abstract'] = article.abstract
            dic['have_img'] = str(article.have_img)
            last_time = article.last_modified_time
            dic['last_modified_time'] = str(last_time.year) + "-" + str(last_time.month) + '-' + \
                                        str(last_time.day) + ' ' + str(last_time.hour) + ':' + \
                                        str(last_time.minute) + ':' + str(last_time.second)
            dic['words'] = article.words
            dic['views'] = article.views
            dic['comments'] = article.comments
            dic['love'] = article.love
            dic['user_name'] = article.author.userinfo.name
            article_list.append(dic)
        if article_list:
            offset += 1
            if_have = True
        content = {
            "offset": offset,
            "article": article_list,
            "status": if_have
        }
        return HttpResponse(dumps(content))


def change_recommend_author(request):
    if request.method == 'GET':
        if request.user.is_anonymous:
            recommend_author = UserInfo.objects.all().order_by('-words', '-fans', '-loved')[5:10]
        else:
            recommend_author = UserInfo.objects.all().exclude(user__followed__following=request.user).order_by('-words', '-fans', '-loved')[5:10]
        authors = []
        for author in recommend_author:
            if author.words > 999:
                author.words = str(round(author.words / 1000, 1)) + 'k'
            else:
                author.words = str(author.words)
            if author.loved > 999:
                author.loved = str(round(author.loved / 1000, 1)) + 'k'
            else:
                author.loved = str(author.loved)
            dic = {}
            dic['id'] = author.user_id
            dic['name'] = author.name
            dic['head_img'] = str(author.head_img)
            dic['words'] = author.words
            dic['loved'] = author.loved
            authors.append(dic)
        content = {
            "authors": authors
        }
        return HttpResponse(dumps(content))


def get_main_page(request):
    if request.method == 'GET':
        user_id = request.user.id
        try:
            user_info = UserInfo.objects.get(user_id=user_id)
        except UserInfo.DoesNotExist:
            user_info = UserInfo()
        if request.GET.get('user', None):
            user_id = request.GET.get('user')
        other_user = UserInfo.objects.get(user_id=user_id)
        content = {"user_info": user_info, "other_user": other_user}
        return render(request, 'bbs/info.html', content)


def save_introduction(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        intro = request.POST.get('intro')
        user = UserInfo.objects.get(id=user_id)
        user.intro = intro
        user.save()
        content = {
            "status": 1
        }
        return HttpResponse(dumps(content))


def collect_article(request):
    if request.method == 'GET':
        try:
            user_info = UserInfo.objects.get(user_id=request.user.id)
        except UserInfo.DoesNotExist:
            user_info = UserInfo()
        user = User.objects.get(id=request.user.id)
        article = user.collect.all()
        content = {
            "user_info": user_info,
            "article": article
        }
        return render(request, 'bbs/collection.html', content)
    elif request.method == 'POST':
        article_id = int(request.POST.get('article_id'))
        article = Article.objects.get(id=article_id)
        if article.collects.filter(id=request.user.id):
            article.collects.remove(request.user)
            status = 0
        else:
            article.collects.add(request.user)
            status = 1
        content = {
            "status": status
        }
        return HttpResponse(dumps(content))


def love_article(request):
    if request.method == 'GET':
        user_id = request.user.id
        try:
            user_info = UserInfo.objects.get(user_id=user_id)
        except UserInfo.DoesNotExist:
            user_info = UserInfo()
        if request.GET.get('user', None):
            user_id = request.GET.get('user')
        other_user = UserInfo.objects.get(user_id=user_id)
        article = User.objects.get(id=user_id).love.all()
        content = {
            "user_info": user_info,
            "article": article,
            "other_user": other_user
        }
        return render(request, 'bbs/loved.html', content)
    elif request.method == 'POST':
        article_id = int(request.POST.get('article_id'))
        article = Article.objects.get(id=article_id)
        user = UserInfo.objects.get(user=article.author)
        if article.loves.filter(id=request.user.id):
            with transaction.atomic():
                article.loves.remove(request.user)
                article.love = article.love - 1
                article.save()
                user.loved -= 1
                user.save()
            status = 0
        else:
            with transaction.atomic():
                article.loves.add(request.user)
                article.love = article.love + 1
                article.save()
                user.loved += 1
                user.save()
            status = 1
        content = {
            "status": status
        }
        return HttpResponse(dumps(content))


@login_required(login_url='bbs/../../signup')
def setting_basic(request):
    if request.method == 'GET':
        try:
            user_info = UserInfo.objects.get(user_id=request.user.id)
        except UserInfo.DoesNotExist:
            user_info = UserInfo()
        content = {
            "user_info": user_info
        }
        return render(request, 'bbs/basic.html', content)


def img_save(file, root):
    save_path = get_img_path(root)
    img_suffixes = ['jpg', 'jpeg', 'png', 'gif', 'jfif', 'bmp']
    from uuid import uuid1
    img_suffix = file.name.split(".")[-1]
    if img_suffix.lower() not in img_suffixes:
        img_suffix = 'jpg'
    file_name = str(uuid1()) + "." + img_suffix
    save_path = save_path + file_name
    with open(save_path, 'wb') as img:
        for f in file.chunks():
            img.write(f)
    crop_img(open_path=save_path)
    return save_path


def change_head_img(request):
    if request.method == 'POST':
        file = request.FILES.get("head_img", None)
        if file:
            save_path = img_save(file, 'head')
            user_id = request.POST.get("id")
            user = UserInfo.objects.get(id=user_id)
            user.head_img = save_path.split("media\\")[-1]
            user.save()
            status = 1
            url = save_path.split("jianshu\\")[-1]
            content = {
                "status": status,
                "url": url
            }
        else:
            status = 0
            content = {
                "status": status,
            }
        return HttpResponse(dumps(content))


def iden_code_data():
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numcase = '0123456789'
    i = 0
    code_data = ''
    while i < 6:
        num = random.choice([0, 1, 2])
        if num == 0:
            code = random.choice(lowercase)
        elif num == 1:
            code = random.choice(uppercase)
        else:
            code = random.choice(numcase)
        code_data += code
        i += 1
    return code_data


def send_email_security_code(request, email):
    user_id = request.POST.get('id')
    host = request.get_host()
    user = UserInfo.objects.get(id=user_id)
    username = str(user.name)
    emails = []
    emails.append(email)
    code = iden_code_data()
    session_id = str(user_id) + str(email)
    request.session[session_id] = code
    request.session.set_expiry(10 * 60)
    subject = '简书重要操作验证码'
    text_content = r'与诗 您好\n请使用下面的验证码验证您的操作，验证码 10 分钟内有效:\n044698\n\n©2012-2019 上海与诗创作公司 / 简书 / 沪ICP备11018329号-5 / '
    html_content = '<div style="position: relative;font-size: 14px;height: auto;padding: 15px 15px 10px 15px">' + '<div class="main" style="background-color:#D3D3D3;padding:30px 10% 70px 10%;">' + '<div class="header" style="padding: 20px 0;">' + '<a href="首页地址"><img src="img/logo.png" style="height:40px;"/></a>' + '</div>' + '<div class="content" style="overflow: hidden;padding:30px 10% 70px 10%;margin:0 10%;background-color: #fff;box-shadow:0 4px 20px rgba(0,0,0,0.1);word-break: break-all;">' + '<h2 style="margin: 30px 0;">与诗 您好</h2>' + '<p style="margin-bottom: 40px;">请使用下面的验证码验证您的操作，验证码 10 分钟内有效:</p>' + '<span style="padding: 10px 20px; font-size: 24px;background-color: #EB6F5A;border-radius:4px;color:#fff;">444444</span>' + '</div>' + '</div>' + '<div class="footer" style="padding:10px 20px;background-color:#333;font-size:12px;color: #999 ">' + '<p>©<span style="border-bottom:1px dashed #ccc;z-index:1">2012-2019</span> 上海与诗创作公司 / 简书 / 沪ICP备' + '<span style="border-bottom: 1px dashed rgb(204, 204, 204); z-index: 1; position: static;">11018329</span>号-5 / </p>' + '</div></div>'
    html_content = html_content.replace("与诗", username).replace("img/logo.png",
                    "http://" + host + '/static/img/logo.png').replace("444444", code).replace("首页地址", "http://" + host)
    msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def bind_email_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email__iexact=email):
            status = 0
            message = "该邮箱已经被绑定，无法重复绑定"
        else:
            send_email_security_code(request, email)
            status = 1
            message = "验证码发送成功"
        content = {
            "status": status,
            "message": message
        }
        return HttpResponse(dumps(content))


def bind_email(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        email = request.POST.get('email')
        code = request.POST.get('code')
        session_id = str(user_id) + str(email)
        if request.session.get(session_id).lower() == code.lower():
            user = User.objects.get(id=UserInfo.objects.get(id=user_id).user_id)
            user.email = email
            user.save()
            del request.session[session_id]
            status = 1
            message = "绑定成功"
        else:
            status = 0
            message = "验证码错误，绑定失败，请在有效期内重新输入"
        content = {
            "status": status,
            "message": message
        }
        return HttpResponse(dumps(content))


def unbind_email_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        send_email_security_code(request, email)
        status = 1
        message = "验证码发送成功"
        content = {
            "status": status,
            "message": message
        }
        return HttpResponse(dumps(content))


def unbind_email(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        email = request.POST.get('email')
        code = request.POST.get('code')
        session_id = str(user_id) + str(email)
        if request.session.get(session_id).lower() == code.lower():
            user = User.objects.get(id=UserInfo.objects.get(id=user_id).user_id)
            user.email = ""
            user.save()
            del request.session[session_id]
            status = 1
            message = "绑定成功"
        else:
            status = 0
            message = "验证码错误，取消绑定失败，请在有效期内重新输入"
        content = {
            "status": status,
            "message": message
        }
        return HttpResponse(dumps(content))


def bind_phone_code(request):
    if request.method == 'POST':
        content = {
            "status": 1,
            "message": '此功能暂未开发，敬请期待'
        }
        return HttpResponse(dumps(content))


def bind_phone(request):
    if request.method == 'POST':
        content = {
            "status": 1,
            "message": '此功能暂未开发，敬请期待'
        }
        return HttpResponse(dumps(content))


def basic_save(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        name = request.POST.get('username')
        if UserInfo.objects.filter(name=name):
            status = 0
            message = "昵称已被占用，请重新修改一个"
        else:
            user = UserInfo.objects.get(id=user_id)
            user.name = name
            user.save()
            status = 1
            message = "昵称修改成功"
        content = {
            "status": status,
            "message": message
        }
        return HttpResponse(dumps(content))


def bind_wechat(request):
    if request.method == 'POST':
        file = request.FILES.get("wechat", None)
        if file:
            save_path = img_save(file, 'wechat')
            user_id = request.POST.get("id")
            user = UserInfo.objects.get(id=user_id)
            user.wechatimg = save_path.split("media\\")[-1]
            user.save()
            status = 1
            url = save_path.split("jianshu\\")[-1]
            content = {
                "status": status,
                "url": url
            }
        else:
            content = {
                "status": 0
            }
        return HttpResponse(dumps(content))


def profile_save(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        sex = request.POST.get('sex')
        intro = request.POST.get('intro')
        web = request.POST.get('web')
        status = 1
        try:
            user = UserInfo.objects.get(id=user_id)
            user.sex = sex
            user.intro = intro
            user.website = web
            user.save()
        except UserInfo.DoesNotExist:
            status = 0
        finally:
            content = {
                "status": status
            }
            return HttpResponse(dumps(content))


@login_required(login_url='bbs/../../signup')
def setting_profile(request):
    if request.method == 'GET':
        try:
            user_info = UserInfo.objects.get(user_id=request.user.id)
        except UserInfo.DoesNotExist:
            user_info = UserInfo()
        content = {
            "user_info": user_info
        }
        return render(request, 'bbs/profile.html', content)


def get_following_article(request):
    if request.method == 'GET':
        try:
            user_info = UserInfo.objects.get(user_id=request.user.id)
        except UserInfo.DoesNotExist:
            user_info = UserInfo()
        friends = FriendShip.objects.filter(following=request.user).exclude(followed=request.user)
        article = Article.objects.filter(author__followed__following=request.user).order_by('-last_modified_time')[:6]
        content = {
            "user_info": user_info,
            "followers": friends,
            "article": article
        }
        return render(request, 'bbs/follow.html', content)


def load_more_follow_article(request):
    if request.method == 'GET':
        offset = int(request.GET.get("offset"))
        articles = Article.objects.filter(author__followed__following=request.user).order_by('-last_modified_time')[offset * 6:(offset + 1) * 6]
        article_list = []
        if_have = False
        for article in articles:
            dic = {}
            dic['id'] = article.id
            dic['title'] = article.title
            dic['abstract'] = article.abstract
            dic['have_img'] = str(article.have_img)
            last_time = article.last_modified_time
            dic['last_modified_time'] = str(last_time.year) + "-" + str(last_time.month) + '-' + \
                                        str(last_time.day) + ' ' + str(last_time.hour) + ':' + \
                                        str(last_time.minute) + ':' + str(last_time.second)
            dic['words'] = article.words
            dic['views'] = article.views
            dic['comments'] = article.comments
            dic['love'] = article.love
            dic['user_name'] = article.author.userinfo.name
            article_list.append(dic)
        if article_list:
            offset += 1
            if_have = True
        content = {
            "offset": offset,
            "article": article_list,
            "status": if_have
        }
        return HttpResponse(dumps(content))


def set_following(request):
    if request.method == 'POST':
        follower = request.user
        if follower.is_anonymous:
            status = 0
            url = "http://" + request.get_host() + '/bbs/signup'
            return HttpResponse(dumps({"status": status,"url": url}))
        else:
            followed = User.objects.get(id=int(request.POST.get('followed')))
            like = UserInfo.objects.get(user=follower)
            fans = UserInfo.objects.get(user=followed)
            with transaction.atomic():
                FriendShip.objects.create(following=follower, followed=followed)
                if like == fans:
                    like.like += 1
                    like.fans += 1
                    like.save()
                else:
                    like.like += 1
                    like.save()
                    fans.fans += 1
                    fans.save()
            status = 1
            content = {
                "status": status,
            }
            return HttpResponse(dumps(content))


def cancel_following(request):
    if request.method == 'POST':
        follower = request.user
        followed = User.objects.get(id=int(request.POST.get('followed')))
        like = UserInfo.objects.get(user=follower)
        fans = UserInfo.objects.get(user=followed)
        with transaction.atomic():
            FriendShip.objects.get(following=follower, followed=followed).delete()
            if like == fans:
                like.like -= 1
                like.fans -= 1
                like.save()
            else:
                like.like -= 1
                like.save()
                fans.fans -= 1
                fans.save()
        status = 1
        content = {
            "status": status
        }
        return HttpResponse(dumps(content))


def submit_comment(request):
    if request.method == 'POST':
        if request.user.is_anonymous:
            url = "http://" + request.get_host() + '/bbs/signup'
            return HttpResponse(dumps({"status": -1, "url": url}))
        else:
            article_id = request.POST.get('article_id', None)
            if article_id:
                try:
                    article = Article.objects.get(id=article_id)
                    article.comments += 1
                    article.save()
                    text = request.POST.get('text')
                    comment = Comments.objects.create(author=request.user, article=article, content=text)
                    dic = {}
                    dic['uid'] = str(comment.author_id)
                    dic['head_img'] = str(request.user.userinfo.head_img)
                    dic['id'] = str(comment.id)
                    dic['name'] = request.user.userinfo.name
                    dic['text'] = comment.content
                    submit_time = comment.submit_date
                    dic['submit_time'] = str(submit_time.year) + "." + str(submit_time.month) + '.' + \
                                                str(submit_time.day) + ' ' + str(submit_time.hour) + ':' + \
                                                str(submit_time.minute)
                    status = 1
                    content = {"status": status, "comment": dic}
                except Article.DoesNotExist:
                    status = 0
                    content = {"status": status}
                return HttpResponse(dumps(content))
            return HttpResponse(dumps({"status": 0}))


def submit_reply(request):
    if request.method == 'POST':
        if request.user.is_anonymous:
            url = "http://" + request.get_host() + '/bbs/signup'
            return HttpResponse(dumps({"status": -1, "url": url}))
        else:
            try:
                article_id = request.POST.get('article_id', None)
                article = Article.objects.get(id=article_id)
                article.comments += 1
                article.save()
                text = request.POST.get('text', None)
                comment_id = request.POST.get('comment_id', None)
                comment = Comments.objects.get(id=comment_id)
                author_to_id = request.POST.get('author_to_id', None)
                author_to = User.objects.get(id=author_to_id)
                author_from = request.user
                reply = CommentsReply.objects.create(article=article, comment=comment, content=text, author_from=author_from, author_to=author_to)
                dic = {}
                dic['uid'] = reply.author_from.id
                dic['id'] = reply.id
                dic['name'] = reply.author_from.userinfo.name
                dic['author_to'] = reply.author_to.userinfo.name
                dic['text'] = reply.content
                content = {
                    "status": 1,
                    "reply": dic
                }
            except Exception:
                content = {"status": 0}
            return HttpResponse(dumps(content))


def thumbs_up(request):
    if request.method == 'POST':
        if request.user.is_anonymous:
            url = "http://" + request.get_host() + '/bbs/signup'
            return HttpResponse(dumps({"status": -1, "url": url}))
        else:
            is_reply = request.POST.get('is_reply')
            if is_reply == 'true':
                reply = CommentsReply.objects.get(id=request.POST.get('comment_id'))
                if reply.thumbsup.filter(id=request.user.id):
                    reply.thumbsup.remove(request.user)
                else:
                    reply.thumbsup.add(request.user)
                reply.save()
            else:
                comment = Comments.objects.get(id=request.POST.get('comment_id'))
                if comment.thumbsup.filter(id=request.user.id):
                    comment.thumbsup.remove(request.user)
                else:
                    comment.thumbsup.add(request.user)
                comment.save()
            return HttpResponse(dumps({"status": 1}))