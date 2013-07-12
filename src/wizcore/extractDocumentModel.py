#coding=utf-8
import jieba.posseg as pseg
words = pseg.cut(u'我爱北京天安门，在这里真好，的')
for w in words:
    print w.word, w.flag
