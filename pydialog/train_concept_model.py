import json
import dill

import sklearn_crfsuite
from crf_utils import load_data, word2feature, sent2features, sent2label

# dataの読み込み
sents = load_data("./data/concept_samples.dat")

# 各単語の情報を素性に変換
# CRFは各単語だけをみるのではなく、周りの(右隣、左隣)単語や品詞を考慮に入れることができる
X = [sent2features(s) for s in sents]

# 各単語のラベル情報
y = [sent2label(s) for s in sents]

# [{'bias': 1.0, 'word': '愛知', 'postag': '名詞', 'BOS': True, 'EOS': True}], ['B-place']
print(X[0], y[0])

# 岩手です => 岩手(B-place) / です (O)
# [{'bias': 1.0, 'word': '岩手', 'postag': '名詞', 'BOS': True, '+1:word': 'です', '+1:postag': '助動詞'},
# {'bias': 1.0, 'word': 'です', 'postag': '助動詞', '-1:word': '岩手', '-1:postag': '名詞', 'EOS': True}], ['B-place', 'O']
print(X[1000], y[1000])

# CRFによる学習
crf = sklearn_crfsuite.CRF(
    algorithm="lbfgs",
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True,
)

crf.fit(X, y)

with open("./data/crf_model", "wb") as f:
    dill.dump(crf, f)
    