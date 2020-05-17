def load_data(path):
    sents = []
    lis = []
    with open(path, "r") as f:
        for line in f:
            line = line.rstrip()
            # 空行で一つの事例が区切ってある
            if line == "":
                sents.append(lis)
                lis = []
            else:
                # 明日	名詞	B-date
                word, postag, label = line.split("\t")
                lis.append([word, postag, label])

    return sents


def word2feature(sent, i):
    # 単語情報から素性を作成
    word = sent[i][0]
    postag = sent[i][1]
    features = {
        "bias":1.0,
        "word":word,
        "postag":postag,
    }
    if i > 0:
        word_left = sent[i - 1][0]
        postag_left = sent[i - 1][1]
        features.update({
            "-1:word":word_left,
            "-1:postag":postag_left,
        })
    else:
        features["BOS"] = True

    if i < len(sent)-1:
        word_right = sent[i + 1][0]
        postag_right = sent[i + 1][1]
        features.update({
            "+1:word":word_right,
            "+1:postag":postag_right,
        })
    else:
        features["EOS"] = True

    return features


def sent2features(sent):
    # 単語情報を素性に変換
    return [word2feature(sent, i) for i in range(len(sent))]

def sent2label(sent):
    #　文情報をラベルに変換
    return [label for word, postag, label in sent]
