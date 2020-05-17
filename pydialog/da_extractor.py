import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import dill

mecab = MeCab.Tagger()
mecab.parse('')

with open("./model/svc.model", "rb") as f:
    vectorizer = dill.load(f)
    label_encoder = dill.load(f)
    svc = dill.load(f)

def extract_da(utt):
    words = []
    for line in mecab.parse(utt).splitlines():
        if line == "EOS":
            break
        else:
            word, feature_str = line.split("\t")
            words.append(word)

    token_str = " ".join(words)

    X = vectorizer.transform([token_str])
    pred = svc.predict(X)
    da = label_encoder.inverse_transform(pred)[0]
    return da

for utt in ["大阪の明日の天気", "もう一度はじめから", "東京じゃなくて"]:
    da = extract_da(utt)
    print(utt, da)

