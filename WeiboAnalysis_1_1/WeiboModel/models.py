import requests
from django.db import models

# Create your models here.
# 热点文章

class HotArticle(models.Model):
    article_bid = models.CharField('文章BID', max_length=100)
    article_uid = models.CharField('文章UID', max_length=100)
    article_id = models.CharField('文章ID', max_length=100)
    screen_name = models.TextField('用户昵称')
    text = models.TextField('微博正文')
    topics = models.TextField('话题')
    publish_time = models.DateTimeField('发布时间')
    location= models.TextField('发布位置')
    comments_count = models.IntegerField('评论数')
    reposts_count = models.IntegerField('转发数')
    publish_tool = models.TextField('发布工具')

    class Meta:
        db_table = "hot_article"
        verbose_name = "热点文章"
        verbose_name_plural = verbose_name
        ordering = ('id',)

# 用户评论
class Comment(models.Model):
    article_uid = models.CharField('文章UID', max_length=100)
    article_id = models.CharField('文章ID', max_length=100)
    username = models.CharField('用户名', max_length=100)
    text = models.TextField('评论内容')
    publish_time = models.DateTimeField('发布时间')
    positive = models.BooleanField('是否积极', null=True, editable=False)
    prob = models.FloatField('积极估计概率', null=True, editable=False)


    def save(self, *args, **kwargs):
        from tools.nlpapi import sentiment
        if self.prob is None:
            prob = sentiment(self.text)
            self.prob = prob
            self.positive = prob >= 0.5
        super(Comment, self).save(*args, **kwargs)

    class Meta:
        db_table = "comment"
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name
        # unique_together = (
        #     ('article_uid', 'article_id'),
        # )
        ordering = ('id',)

