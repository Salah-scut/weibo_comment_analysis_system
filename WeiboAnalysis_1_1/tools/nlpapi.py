from aip import AipNlp

"""
你的 APPID AK SK
每秒钟只能调用两次
"""
APP_ID = '25839928'
API_KEY = 'yaZF8dmbtdW4PO020vWZUHGz'
SECRET_KEY = 'GrxLxfQwkdGvqMG6uYuSrvVbvuziOCpx'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

# bosonnlp情感分析API   改用百度NLP
# def sentiment(text):
#     result = requests.post(
#         'http://static.bosonnlp.com/analysis/sentiment?analysisType=weibo', data=dict(data=text)).json()
#     return result[0][0]

def sentiment(text):
    try:
        judge = client.sentimentClassify(text)  # 判定为空
        positive_prob = judge['items'][0]['positive_prob']
        return positive_prob
    except Exception as e:
        return 0.5

if __name__ == '__main__':
    judge = client.sentimentClassify("今天天气真好")  # 判定为空
    positive_prob = judge['items'][0]['positive_prob']
    print(positive_prob)