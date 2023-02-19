import django
import os
from datetime import datetime
import re
import requests
from requests_html import HTMLSession
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'public_opinion_analysis_system.settings')

django.setup()

dformat = '%a %b %d %H:%M:%S +%f %Y'
del_quote = re.compile(r'\[.*?\]')

def crawl_comments(uid='2656274875', id_='4750929263595486', max_id=None):
    print("获取评论中...")
    from WeiboModel.models import Comment
    session = HTMLSession()
    # https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=4751660058938029&is_show_bulletin=2&is_mix=0&count=10&uid=7474091977
    # https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=4751386769625194&is_show_bulletin=2&is_mix=0&count=10&uid=7744960129
    url = 'https://weibo.com/ajax/statuses/buildComments'
    params = {
        'flow': '1',
        'is_reload': '1',
        'id': id_,
        'is_show_bulletin': '2',
        'is_mix': '0',
        'max_id': max_id,
        'count': '20',
        'uid': uid,
    }
    print(params)

    res = session.get(url, params=params)
    result = res.json()

    # 列表
    print("评论数量：", len(result['data']))
    for i in result['data']:
        print(i)
        publish_time = datetime.strptime(i['created_at'], dformat)
        text = del_quote.sub('', i['text_raw']).replace(
            '！', '').replace('!', '')
        if text:
            try:
                c = Comment.objects.create(
                    article_uid=uid,
                    article_id =id_,
                    username=i['user']['name'],
                    text=text,
                    publish_time=publish_time)
                print(c.__dict__)
            except:
                pass
    print("评论更新完毕")


# def judge():
#     from WeiboModel.models import Comment
#     for c in Comment.objects.filter(positive=None):
#         try:
#             prob = sentiment(c.text)
#         except:
#             prob = 0.5
#         c.prob = prob
#         c.positive = prob >= 0.5
#         c.save()
#         print(c.text, c.prob, c.positive)

def updateDatabase(path):
    """
    更新数据库内容
    """
    from WeiboModel.models import HotArticle
    import csv
    import time
    filename = path
    with open(filename, 'r', encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)   # 跳过表头
        for row in reader:

            t_article_bid = row[1]
            t_article_uid = row[2]
            t_article_id = row[0]
            t_screen_name = row[3]
            t_text = row[4]
            t_topics = row[8]
            t_publish_time = row[12]
            t_location = row[6]
            t_comments_count = row[10]
            t_reposts_count = row[9]
            t_publish_tool = row[13]
            print(t_article_uid, t_article_id, t_comments_count, t_publish_time)

            # timeArray = time.strptime(t_publish_time, "%Y/%m/%d %H:%M")
            # otherStyleTime = time.strftime("%Y-%m-%d %H:%M", timeArray)
            # t_publish_time = otherStyleTime
            try:
                # 存入数据库微博正文表
                c = HotArticle.objects.create(
                    article_bid =t_article_bid,
                    article_uid=t_article_uid,
                    article_id=t_article_id,
                    screen_name = t_screen_name,
                    text = t_text,
                    topics = t_topics,
                    publish_time = t_publish_time,
                    location = t_location,
                    comments_count = t_comments_count,
                    reposts_count = t_reposts_count,
                    publish_tool = t_publish_tool)
                print(c.__dict__)
                time.sleep(1)
                # 存入数据库评论表
                if int(t_comments_count) > 0:
                    crawl_comments(uid=t_article_uid, id_=t_article_id)
                print("\n")
            except  Exception as e:
                import traceback
                traceback.print_exc()
                continue
        print("更新完毕")

def clearDatabase():
    """
    清空微博数据库内容
    """
    from WeiboModel.models import HotArticle,Comment
    HotArticle.objects.all().delete()
    Comment.objects.all().delete()


if __name__ == '__main__':
    # 1、清空数据库内容
    clearDatabase()
    # 2、更新数据库内容
    updateDatabase("./湖北疫情.csv")
    updateDatabase("./database.csv")
