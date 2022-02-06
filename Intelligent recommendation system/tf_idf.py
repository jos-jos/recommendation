import os
import sys
import jieba
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

class Words:
    def __init__(self, sentences, cut=0):
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

        if cut: 
            sent_words = [list(jieba.cut(sent0)) for sent0 in sentences]
            self.document = [" ".join(sent0) for sent0 in sent_words]
        else:
            self.document = sentences


    def vectorizer(self):
        vocabulary_self = set()
        for line in self.document:
            for vocabulary in self.vocabulary:
                if vocabulary in line:
                    vocabulary_self.update(vocabulary)
                    break
        vocabulary_ = TfidfVectorizer(stop_words=list(self.stop_words)).fit(self.document).vocabulary_
        vocabulary_self.update(list(vocabulary_.keys()))
        self.tfidf_model = TfidfVectorizer(vocabulary = list(vocabulary_self)).fit(self.document)


    def get_words(self, rerun=0):
        if ("tfidf_model" not in dir(self)) or rerun:
            self.vectorizer()
        words = self.tfidf_model.get_feature_names()
        return words


    def get_tfidf(self, rerun=0):
        if ("tfidf_model" not in dir(self)) or rerun:
            self.vectorizer()
        array = self.tfidf_model.transform(self.document).toarray()
        return array


    def get_feature(self, rerun=0): 
        feature = {}
        if ("tfidf_model" not in dir(self)) or rerun:
            self.vectorizer()
        words = self.get_words()
        array = self.get_tfidf()
        for i in range(len(array)):
            for j in range(len(words)):
                if words[j] not in feature:
                    feature[words[j]] = array[i][j]
                else:
                    feature[words[j]] = max(feature[words[j]], array[i][j])
        self.feature = feature
        return feature


    def add_vocabulary(self, words_list, if_save=0):
        self.vocabulary.update(words_list)
        if if_save:
            self._save()


    def add_stop_words(self, words_list, if_save=0):
        self.stop_words.update(words_list)
        if if_save:
            self._save()
    

    def similarity(self, target_axis=0):
        result = []
        array = self.get_tfidf()
        target = array[target_axis]
        array = np.delete(array, target_axis, 0)
        for i in range(len(array)):
            result.append(self._cosine(target, array[i]))
        self.results = result
        return result
    

    def _cosine(self, x, y):
        num = x.dot(y.T)
        denom = np.linalg.norm(x) * np.linalg.norm(y)
        return num / denom


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
    text = [
            "我很喜欢学习，也很喜欢看书，所以我的成绩很好。",
            "由于我很喜欢学习，并且喜欢看书，所以我可以获得很好的成绩。",
            "由于我很喜欢学习，并且喜欢看书，可惜我可以获得很好的成绩。",
            "虽然我很喜欢学习，并且喜欢看书，但是我没有获得过好成绩。"
    ]
    words = Words(text, cut=1)
    print(words.get_words())
    print(words.get_tfidf())
    print(words.get_feature())
    print(words.similarity(2))
