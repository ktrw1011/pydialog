import MeCab
import json
import dill
import sklearn_crfsuite
from crf_utils import word2feature, sent2features, sent2label
import re


mecab = MeCab.Tagger()
mecab.parse("")

with open("./data/crf_model", "rb") as f:
    crf = dill.load(f)

def extract_concept(utt):
    lis = []
    for line in mecab.parse(utt).splitlines():
        if line == "EOS":
            break
        else:
            word, feature_str = line.split("\t")
            features = feature_str.split(",")
            postag = features[0]
            lis.append([word, postag, "O"])

    words = [x[0] for x in lis]
    X = [sent2features(s) for s in [lis]]

    label = crf.predict(X)[0]

    print(words, label)

    # 単語列とラベル系列の対応とって辞書にに変換
    conceptdic = {}
    buf = ""
    last_label = ""
    for word, label in zip(words, label):
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

if __name__ == "__main__":
    for utt in ["大阪の明日の天気", "もう一度はじめから", "東京じゃなくて", "三重です"]:
        conceptdic = extract_concept(utt)
        # ['三', '重', 'です'] ['B-place', 'I-place', 'O']
        # {'place': '三重'}
        print(conceptdic)