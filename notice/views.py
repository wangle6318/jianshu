from django.shortcuts import render, redirect, HttpResponse
from bbs.models import Comments, CommentsReply, UserInfo, User, Article, FriendShip
from notifications.models import Notification, NotificationQuerySet
from django.contrib.auth.views import login_required
from django.db import transaction
import json


@login_required(login_url='/bbs/signup')
def get_comment_list(request):
    if request.method == 'GET':
        user_info = UserInfo.objects.get(user=request.user)
        notice_comments = Notification.objects.filter(recipient=request.user, verb__in=['评论了你', '回复了你'])
        unread_count_comment = notice_comments.filter(unread=True).count()
        notice_follows = Notification.objects.filter(recipient=request.user, verb='关注了你')
        unread_count_follow = notice_follows.filter(unread=True).count()
        context = {"notice_comments": notice_comments, "user_info": user_info,
                   "unread_count_comment": unread_count_comment, "unread_count_follow": unread_count_follow}
        return render(request, 'notice/notice_comments.html', context)


def comment_notice_update(request):
    if request.method == 'GET':
        notice_id = request.GET.get('notice_id')
        if notice_id:
            notice = Notification.objects.get(id=notice_id)
            notice.mark_as_read()
            if notice.verb == '评论了你':
                comment = Comments.objects.get(article=notice.target, content=notice.description, author=notice.actor)
                return redirect('/bbs/article/' + str(notice.target.id) + '#comment-' + str(comment.id))
            else:
                return redirect('/bbs/article/' + str(notice.target.article.id) + '#comment-' + str(notice.target.id))
        else:
            notices = Notification.objects.filter(recipient=request.user, verb__in=['评论了你', '回复了你'], unread=True)
            for notice in notices:
                notice.mark_as_read()
            return redirect("notice:notice_comment_list")


def get_likes_and_thumbs_up_list(request):
    return render(request, 'notice/notice_likes.html')


@login_required(login_url='/bbs/signup')
def get_follow_list(request):
    if request.method == 'GET':
        user_info = UserInfo.objects.get(user=request.user)
        notice_comments = Notification.objects.filter(recipient=request.user, verb__in=['评论了你', '回复了你'])
        unread_count_comment = notice_comments.filter(unread=True).count()
        notice_follows = Notification.objects.filter(recipient=request.user, verb='关注了你')
        unread_count_follow = notice_follows.filter(unread=True).count()
        has_followed = FriendShip.objects.filter(following=request.user).values_list("followed_id")
        has_followed = [x[0] for x in has_followed]
        context = {"notice_follows": notice_follows, "user_info": user_info,
                   "unread_count_follow": unread_count_follow,
                   "unread_count_comment": unread_count_comment, "has_followed": has_followed}
        return render(request, 'notice/notice_follows.html', context)


def follow_notice_update(request):
    notices = Notification.objects.filter(recipient=request.user, verb='关注了你', unread=True)
    for notice in notices:
        notice.mark_as_read()
    return redirect("notice:notice_follow_list")


def set_following(request):
    following = request.user
    if following.is_anonymous:
        return redirect("bbs:signup")
    else:
        followed_id = request.POST.get('followed_id')
        followed = User.objects.get(id=followed_id)
        like = UserInfo.objects.get(user=following)
        fans = UserInfo.objects.get(user=followed)
        with transaction.atomic():
            FriendShip.objects.create(following=following, followed=followed)
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
        return HttpResponse(json.dumps(content))


def cancel_following(request):
    following = request.user
    if following.is_anonymous:
        return redirect("bbs:signup")
    followed_id = request.POST.get('followed_id')
    followed = User.objects.get(id=followed_id)
    like = UserInfo.objects.get(user=following)
    fans = UserInfo.objects.get(user=followed)
    with transaction.atomic():
        FriendShip.objects.get(following=following, followed=followed).delete()
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
    return HttpResponse(json.dumps(content))