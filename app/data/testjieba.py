import jieba
import jieba.posseg as pseg
jieba.set_dictionary('dict.txt.big')

try:
    while True:
        line = input()
        words = pseg.cut(line)
        for word, flag in words:
            print('%s %s' % (word, flag))
except:
    pass
        
