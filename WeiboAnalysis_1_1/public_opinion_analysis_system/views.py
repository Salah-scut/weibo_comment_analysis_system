import json

from django.shortcuts import redirect, render
from WeiboModel.models import Comment,HotArticle
from public_opinion_analysis_system.data import ChartData


def index(request):
    print(request.COOKIES.get('is_login'))
    # status = request.COOKIES.get('is_login')  # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的 cookie
    # if not status:
    #     return redirect('/login/')
    return render(request, "index.html")

def weibo_comment(request):
    context = {}
    comment_list = Comment.objects.all()
    context['comment_list'] = comment_list
    return render(request, "weibo_comment.html", context)


def weibo_hot_article(request):
    context = {}
    name_list = ['用户昵称', '微博正文', '话题', '发布时间',
                    '发布位置', '评论数', '转发数']
    article_list = HotArticle.objects.all()
    context['article_list'] = article_list
    context['name_list'] = name_list
    return render(request, "weibo_hot_article.html", context)

def chart(request):
    form = ChartData()
    title = "网络舆情热点评估与分析"
    return render(request, "chart.html", locals())
