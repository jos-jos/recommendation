import os
import sys
import jieba
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

class Words:
    def __init__(self):
        self.file_name = os.path.join(sys.path[0], "data/KeyWords.csv")
        with open(self.file_name, "r", encoding='utf-8') as f:
            text = [i.replace("\n", "").split(",") for i in f.readlines()]
        self.vocabulary = set()
        self.stop_words = set()
        for line in text:
            if line[0] == "vocabulary":
                self.vocabulary.update(line[1:])
            elif line[0] == "stop_words":
                self.stop_words.update(line[1:])

    def get_words(self, text):
        sentences = text.split()
        sent_words = [list(jieba.cut(sent0)) for sent0 in sentences]
        document = [" ".join(sent0) for sent0 in sent_words]

        vocabulary_self = list(self.vocabulary)
        vocabulary_ = TfidfVectorizer(stop_words=list(self.stop_words)).fit(document).vocabulary_
        vocabulary_len = len(vocabulary_)
        index = 0
        for i in range(len(self.vocabulary)):
            if vocabulary_self[i] not in vocabulary_.keys():
                vocabulary_[vocabulary_self[i]] = vocabulary_len + index
                index+=1
        tfidf_model = TfidfVectorizer(vocabulary = vocabulary_).fit(document)
        words = tfidf_model.get_feature_names()
        return words

    def add_vocabulary(self, words_list, if_save=0):
        self.vocabulary.update(words_list)
        if if_save:
            self._save()

    def add_stop_words(self, words_list, if_save=0):
        self.stop_words.update(words_list)
        if if_save:
            self._save()
    
    def _save(self):
        vocabulary_line = ",".join(list(self.vocabulary))
        stop_words_line = ",".join(list(self.stop_words))
        with open(self.file_name, "w", encoding='utf-8') as f:
            f.write("vocabulary,")
            f.write(vocabulary_line)
            f.write("\n")
            f.write("stop_words,")
            f.write(stop_words_line)


if __name__ == "__main__":
    text = """
    "你好啊，我是呼呼，我觉得我很好，你觉得呢？我学过C语言，C++，Java，mysql，android还有硬件设计等等，我比较擅长模型编译部署等工作"
    """
    words = Words()
    words.add_vocabulary(["Java"], if_save=1)
    words.add_stop_words(["觉得", "还有"], if_save=1)
    print(words.get_words(text))
