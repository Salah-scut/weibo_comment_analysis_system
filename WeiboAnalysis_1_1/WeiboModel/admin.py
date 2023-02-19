from django.contrib import admin
from WeiboModel.models import Comment,HotArticle

# Register your models here.
admin.site.site_header = '基于情感分析的网络舆情热点评估与分析系统后台'  # 设置header
admin.site.site_title = '基于情感分析的网络舆情热点评估与分析系统后台'  # 设置title
admin.site.index_title = '基于情感分析的网络舆情热点评估与分析系统后台'

# add 按钮指定字段显示  将输入栏分块，每个栏也可以定义自己的格式
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','article_uid', 'article_id','username', 'text', 'publish_time', 'positive', 'prob')  # 定义该页面的显示，比如在列表中显示更多的栏目，只需要在 ContactAdmin 中增加 list_display 属性
    search_fields = ('article_uid', 'article_id','username','text', 'publish_time', 'positive')  # 搜索功能在管理大量记录时非常有，我们可以使用 search_fields 为该列表页增加搜索栏

class HotArticleAdmin(admin.ModelAdmin):
    """
    article_bid = models.CharField('BID', max_length=100)
    article_uid = models.CharField('UID', max_length=100)
    article_id = models.CharField('ID', max_length=100)
    screen_name = models.TextField('用户昵称')
    text = models.TextField('微博正文')
    topics = models.TextField('话题')
    publish_time = models.DateTimeField('发布时间')
    location= models.TextField('发布位置')
    comments_count = models.IntegerField('评论数')
    reposts_count = models.IntegerField('转发数')
    publish_tool = models.TextField('发布工具')
    """
    list_display = ('id', 'article_uid', 'article_id', 'screen_name', 'text', 'topics',
                    'publish_time', 'location', 'comments_count',
                    'reposts_count', 'publish_tool')
    search_fields = ('article_uid', 'article_id','screen_name','text', 'topics')


admin.site.register(HotArticle, HotArticleAdmin)
admin.site.register(Comment, CommentAdmin)
