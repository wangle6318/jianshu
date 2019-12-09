from django.db.models.signals import post_save
from notifications.signals import notify
from bbs.models import Comments, CommentsReply, Article, FriendShip
from django.contrib.auth.models import User


def comment_handle(sender, instance, created, **kwargs):
    recipients = User.objects.exclude(id=instance.author.id)
    if instance.article.author in recipients:
        notify.send(sender=instance.author,
                    recipient=instance.article.author,
                    verb='评论了你',
                    target=instance.article,
                    description=instance.content)


post_save.connect(comment_handle, sender=Comments)


def reply_handle(sender, instance, created, **kwargs):
    recipients = User.objects.exclude(id=instance.author_from.id)
    if instance.author_to in recipients:
        notify.send(sender=instance.author_from,
                    recipient=instance.author_to,
                    verb='回复了你',
                    target=instance.comment,
                    description=instance.content)


post_save.connect(reply_handle, sender=CommentsReply)


# def love_article_handle(sender, instance, created, **kwargs):
#     recipients = User.objects.exclude(id=instance.user.id)
#     if instance.article.author_id in recipients:
#         notify.send(sender=instance.user,
#                     recipient=instance.article.author,
#                     verb='喜欢了你的文章',
#                     target=instance.article)
#
#
# post_save.connect(love_article_handle, sender=Article.love)


def follow_handle(sender, instance, created, **kwargs):
    recipients = User.objects.exclude(id=instance.following.id)
    if instance.followed in recipients:
        following = instance.following
        followed = instance.followed
        notices = followed.notifications.filter(verb='关注了你')
        notice = None
        for n in notices:
            if following == n.actor:
                notice = n
                break
        if notice:
            notice.delete()
        notify.send(sender=instance.following, recipient=instance.followed, verb='关注了你')


post_save.connect(follow_handle, sender=FriendShip)