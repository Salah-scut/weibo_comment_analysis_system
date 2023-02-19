# -*- coding: utf-8 -*-

from django.db.models import Q

from WeiboModel.models import Comment, HotArticle
from tools.topic_statistical import clearTxt, getWordCount, sent2word


class SourceDataDemo:

    def __init__(self):
        # 默认的标题
        self.title = '数据可视化'
        # 两个小的form看板
        self.counter = {'name': '正面情感数量', 'value': 342}
        self.counter2 = {'name': '负面情感数量', 'value': 29}
        self.counter3 =  {'name': '中性情感数量', 'value': 29}

        # 总共是6个图表，数据格式用json字符串，其中第3个图表是有3个小的图表组成的
        self.echart1_data = {
            'title': '情感概率分布',
            'data': [
                {"name": "0-20%", "value": 12},
                {"name": "20-40%", "value": 23},
                {"name": "40-60%", "value": 90},
                {"name": "60-80%", "value": 84},
                {"name": "80-100%", "value": 84},
            ]
        }

        self.word_cloud = {
            'title': '微博热点话题',
            'data':[
                { "name": "共抗疫情","value": 1446},
                {"name": "上海疫情", "value": 928 },
                {"name": "天津身边事","value": 906},
                {"name": "网购商品","value": 825},
                {"name": "东航MU5735航班","value": 514},
                {"name": "天津疫情","value": 486},
                {"name": "学校因疫情防控","value": 53 },
            ]
        }

    @property
    def echart1(self):
        data = self.echart1_data
        echart = {
            'title': data.get('title'),
            # 第一次get获取到的是许多键值对，所以需要对每个键值对再次get
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')]
        }
        # 返回的是标题和对应的数据，并没有说用什么方式展现！
        return echart

    @property
    def wordCloud(self):
        data = self.word_cloud
        echart = {
            'title': data.get('title'),
            'data': data.get('data'),
        }
        return echart


class ChartData(SourceDataDemo):

    def __init__(self):
        """
        按照 SourceDataDemo 的格式覆盖数据即可
        """
        super().__init__()
        try:
            comment_list = Comment.objects.filter(Q(prob__gte=0.0) & Q(prob__lt=0.4))
            comment_list2 = Comment.objects.filter(Q(prob__gte=0.4) & Q(prob__lt=0.6))
            comment_list3 = Comment.objects.filter(Q(prob__gte=0.6) & Q(prob__lt=1.0))
            self.counter = {'name': '正面情感数量', 'value': len(comment_list3)}
            self.counter2 = {'name': '负面情感数量', 'value': len(comment_list)}
            self.counter3 = {'name': '中性情感数量', 'value': len(comment_list2)}

            comment_list2 = Comment.objects.filter(Q(prob__gte=0.0) & Q(prob__lt=0.20))
            comment_list3 = Comment.objects.filter(Q(prob__gte=0.20) & Q(prob__lt=0.40))
            comment_list4= Comment.objects.filter(Q(prob__gte=0.40) & Q(prob__lt=0.60))
            comment_list5 = Comment.objects.filter(Q(prob__gte=0.60) & Q(prob__lt=0.80))
            comment_list6 = Comment.objects.filter(Q(prob__gte=0.80) & Q(prob__lt=1.0))
            self.echart1_data = {
                'title': '情感概率分布',
                'data': [
                    {"name": "0-20%", "value": len(comment_list2)},
                    {"name": "20-40%", "value": len(comment_list3)},
                    {"name": "40-60%", "value": len(comment_list4)},
                    {"name": "60-80%", "value":  len(comment_list5)},
                    {"name": "80-100%", "value":  len(comment_list6)},
                ]
            }
        except Exception as e:
            print("Comment数据库操作失败")
            import traceback
            traceback.print_exc()

        try:
            data_list = []
            topics_list = HotArticle.objects.values("topics")
            words_list = []
            for key in topics_list:
                topics = key["topics"]
                if type(topics) == str and topics !="" and topics != None:
                    line = clearTxt(topics)
                    words = sent2word(line)
                    words_list += words
            words_counts = getWordCount(words_list)
            for name in words_counts:
                if words_counts[name] > 2:
                    dic = {"name": name, "value": words_counts[name]}
                    data_list.append(dic)
            self.word_cloud = {
                'title': '微博热点话题',
                'data': data_list
            }
            print(self.word_cloud)
        except Exception as e:
            print("HotArticle数据库操作失败")
            import traceback
            traceback.print_exc()
