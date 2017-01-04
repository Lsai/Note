from django.conf.urls import patterns, url
from django.template.backends import django

from online import views
from django.conf.urls.static import static
from django.conf import settings


# urlpatterns = patterns('',
#                        url(r'^aaa/$', views.login, name='login'),
#                        url(r'^login/$', views.login, name='login'),
#                        url(r'^regist/$', views.regist, name='register'),
#                        url(r'^index/$', views.index, name='index'),
#                        url(r'^logout/$', views.logout, name='logout'),
#                        url(r'^forgetPwd',views.forgetPwd,name='forgetPwd')
#                     #   url(r'^medias/(?P<path>.*)$','django.views.static.serve',{'document_root':'/'})
#                        )

urlpatterns = [
    url(r'^index/$', views.index,name='index'),
    url(r'^login/$',views.login,name='login'),
    url(r'^regist/$', views.regist, name='register'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^forgetPwd/$',views.forgetPwd,name='forgetPwd'),
    url(r'^identical_code/$',views.identi_code,name='identi_code'),
    url(r'^set_pass/$',views.set_pass,name='set_password'),
    url(r'^article_list/$',views.article_list,name='article_list'),
    url(r'^detail/$',views.detail,name='detail'),
    url(r'^add_book/$',views.add_article,name='add_book'),
    url(r'^add_image/$',views.add_img,name='add_image'),
    url(r'^modify_name/$',views.modify_name,name='modify_name'),
    url(r'^modify_passwd/$',views.modify_passwd,name='modify_passwd'),

]