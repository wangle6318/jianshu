from bbs import views
from bbs.upload import upload_image
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('write', views.publish_article, name='write'),
    path('write/save', views.save_article),
    path('write/get', views.get_article),
    path('write/delete', views.del_article),
    path('upload', upload_image),
    path('article/<int:article_id>', views.article_page, name='article'),
    path('article/submit_comment', views.submit_comment),
    path('article/submit_reply', views.submit_reply),
    path('article/thumbs_up', views.thumbs_up),
    path('load_more_article', views.load_more_article),
    path('change_recommend_author', views.change_recommend_author),
    path('main_page', views.get_main_page, name='my_main_page'),
    path('main_page/save_intro', views.save_introduction),
    path('collection', views.collect_article, name="collection"),
    path('love', views.love_article, name="love"),
    path('setting/basic', views.setting_basic, name="basic"),
    path('setting/basic/head_img', views.change_head_img),
    path('setting/basic/bind_email_code', views.bind_email_code),
    path('setting/basic/bind_email', views.bind_email),
    path('setting/basic/unbind_email_code', views.unbind_email_code),
    path('setting/basic/unbind_email', views.unbind_email),
    path('setting/basic/bind_phone_code', views.bind_phone_code),
    path('setting/basic/bind_phone', views.bind_phone),
    path('setting/basic/save', views.basic_save),
    path('setting/profile', views.setting_profile, name="profile"),
    path('setting/profile/bind_wechat', views.bind_wechat),
    path('setting/profile/save', views.profile_save),
    path('following', views.get_following_article, name="following"),
    path('set_following', views.set_following),
    path('cancel_following', views.cancel_following),
    path('following/load_more_follow_article', views.load_more_follow_article),
]