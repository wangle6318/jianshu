from django.urls import path
from notice import views

urlpatterns = [
    path('comment_notice_list', views.get_comment_list, name='notice_comment_list'),
    path('update_comment_notice', views.comment_notice_update, name='update_comment_notice'),
    path('likes_and_thumbs_up_notice_list', views.get_likes_and_thumbs_up_list, name='notice_likes_list'),
    path('follow_notice_list', views.get_follow_list, name='notice_follow_list'),
    path('update_follow_notice', views.follow_notice_update, name='update_follow_notice'),
    path('follow_notice_list/set_following', views.set_following),
    path('follow_notice_list/cancel_following', views.cancel_following),
]