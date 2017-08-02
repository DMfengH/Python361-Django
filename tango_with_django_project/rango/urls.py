from django.conf.urls import url
from rango import views

# url()函数的第一个参数都是要匹配的正则表达式【小三角表示正则表达式的开始，美元符号表示结束】
# 第二个参数，调用对应的view文件中对应的函数（即网页），处理request。
# 第三个参数，给URL起个名字
urlpatterns = [
    # 什么也没有匹配，即直接使用上一级的url（域名）。什么也没有为什么还要设置？（因为在域名解析的时候，会把url的前面部分去掉再传过来，只剩下空格来匹配）
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category, name='show_category'),
]
