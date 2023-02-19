import re
import jieba

# 停用词，这里自己添加,或者从本地文件读取
stopWords = ["我们","自己","还有","从不","起到","我要","不仅","一名","各种","半点","这是","没有","一个","自己","才能","随着"]


def clearTxt(line:str):
    """
    清洗文本
    """
    if(line != ''):
        line = line.strip()
        # 去除文本中的英文和数字
        line = re.sub("[a-zA-Z0-9]", "", line)
        # 去除文本中的中文符号和英文符号
        line = re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+", "", line)
        return line
    return None



def sent2word(line):
    """
    文本切割
    """
    segList = jieba.cut(line,cut_all=False)
    segSentence = []
    for word in segList:
        if word!="" and word!= None and word != '\t' \
                and word not in stopWords and len(word) != 1:
            segSentence.append(word)
    return segSentence


def getWordCount(words: list):
    """
    词频统计
    """
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts

if __name__ == '__main__':
    line = "我们天色亮了，睁着眼睛想着许多事情。从二月中搬家开始，马上进入房子装修的拆除原结构工程，结果到三月16号被疫情反复按下装修的暂停键，居家封控并做两次核酸检测，一边是小区进出受阻，一边是施工队的电话催促，令我们有一种无名的烦躁情绪在滋生。"
    line = clearTxt(line)
    words = sent2word(line)
    print(getWordCount(words))
