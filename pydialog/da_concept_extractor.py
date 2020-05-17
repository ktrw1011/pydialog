import MeCab
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import dill
import sklearn_crfsuite
from crf_utils import word2feature, sent2features, sent2label
import re

class DAConsept:
    def __init__(self):
        self.mecab = MeCab.Tagger()
        self.mecab.parse("")

        with open("./model/svc.model", "rb") as f:
            self.vectorizer = dill.load(f)
            self.label_encoder = dill.load(f)
            self.svc = dill.load(f)

        with open("./data/crf_model", "rb") as f:
            self.crf = dill.load(f)


    def _parse(self, utt):
        lis = []
        for line in self.mecab.parse(utt).splitlines():
            if line == "EOS":
                break
            else:
                word, feature_str = line.split("\t")
                features = feature_str.split(",")
                postag = features[0]
                lis.append([word, postag, "O"])

        return lis

    def _predict_da(self, lis):
        words = [x[0] for x in lis]
        tokens_str = ' '.join(words)
        X = self.vectorizer.transform([tokens_str])

        pred = self.svc.predict(X)

        da = self.label_encoder.inverse_transform(pred)[0]

        return da

    def _get_concept_dict(self, words, labels):
        conceptdic = {}
        buf = ""
        last_label = ""
        for word, label in zip(words, labels):
            if re.search(r"^B-", label):
                # like "B-place"
                if buf != "":
                    _label = last_label.replace("B-", "").replace("I-", "")
                    conceptdic[_label] = buf

                buf = word

            elif re.search(r"^I-", label):
                # I-で始まる場合は単語を連結
                buf += word

            elif label == "O":
                if buf != "":
                    # ラベルされていないものが出現したらそこで止めて辞書を更新
                    _label = last_label.replace("B-", "").replace("I-", "")
                    conceptdic[_label] = buf
                    buf = ""
                    
            last_label = label

        if buf != "":
            _label = last_label.replace("B-", "").replace("I-", "")
            conceptdic[_label] = buf

        return conceptdic

    def _predict_concept(self, lis):
        words = [x[0] for x in lis]
        X = [sent2features(s) for s in [lis]]
        labels = self.crf.predict(X)[0]

        conceptdic = self._get_concept_dict(words, labels)

        return conceptdic

    def process(self, utt):
        lis = self._parse(utt)
        da = self._predict_da(lis)
        conceptdic = self._predict_concept(lis)

        return da, conceptdic

if __name__ == "__main__":
    da_concept = DAConsept()
    da, conceptdic = da_concept.process("東京の天気は?")
    print(da, conceptdic)


        

        