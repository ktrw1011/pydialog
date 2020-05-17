import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import dill

# MeCabの初期化
mecab = MeCab.Tagger()
mecab.parse("")

sents = []
labels = []

# ファイルの読み込み
with open("./data/da_samples.dat", "r") as f:
    for line in f:
        line = line.strip()
        da, utt = line.split('\t')
        words = []
        for line in mecab.parse(utt).splitlines():
            if line == "EOS":
                break
            else:
                word, feature_str = line.split("\t")
                words.append(word)
        
        sents.append(" ".join(words))
        labels.append(da)

vectorizer = TfidfVectorizer(tokenizer=lambda x: x.split())
X = vectorizer.fit_transform(sents)

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)

svc = SVC(gamma="scale")
svc.fit(X, y)

with open("./model/svc.model", "wb") as f:
    dill.dump(vectorizer, f)
    dill.dump(label_encoder, f)
    dill.dump(svc, f)


