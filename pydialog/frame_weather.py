from da_concept_extractor import DAConsept

# 都道府県のリスト
prefs = [
    '三重', '京都', '佐賀', '兵庫', '北海道', '千葉', '和歌山', '埼玉', '大分',
    '大阪', '奈良', '宮城', '宮崎', '富山', '山口', '山形', '山梨', '岐阜', '岡山',
    '岩手', '島根', '広島', '徳島', '愛媛', '愛知', '新潟', '東京',
    '栃木', '沖縄', '滋賀', '熊本', '石川', '神奈川', '福井', '福岡', '福島', '秋田',
    '群馬', '茨城', '長崎', '長野', '青森', '静岡', '香川', '高知', '鳥取', '鹿児島'
]

# 日付のリスト
dates = ["今日", "明日"]

# 情報種別のリスト
types = ["天気", "気温"]

# システムの対話行為タイプとシステム発話を紐付けた辞書
uttdic = {
    "open-prompt":"ご用件をどうぞ",
    "ask-place": "地名を言ってください",
    "ask-date": "日付を言ってください",
    "ask-type": "情報種別を言ってください",
    }

da_concept = DAConsept()

# 発話から得られた情報を元にフレームを更新
def update_frame(frame, da, conceptdict):
    """
    ユーザーの入力が request-weatherでplace=東京,date=明日の場合には
    da=request-weatherで conceptdict={'place':東京, 'date':明日}になる
    conceptdictの情報を持ってframeを更新する
    """
    # 値の整合性を確認して、整合しないものは空にする
    for k, v in conceptdict.items():
        print(k, v)
        if k == "place" and v not in prefs:
            conceptdict[k] == ""
        elif k == "date" and v not in dates:
            conceptdict[k] == ""
        elif k == "type" and v not in types:
            conceptdict[k] == ""

    if da == "request-weather":
        for k, v in conceptdict.items():
            frame[k] = v
    elif da == "initialize":
        # フレームを初期化
        frame = {"place": "", "date": "", "type": ""}
    elif da == "correct-info":
        # conceptの内容にしたがってフレームを初期化
        for k, v in conceptdict.items():
            if frame[k] == v:
                frame[k] = ""
    
    return frame

def next_system_da(frame):
    # すべてのframe値がからの場合はオープンな対話を始める
    if frame["place"] == "" and frame["date"] == "" and frame["type"] == "":
        return "open-prompt"
    
    #空のスロットがあればその質問を行う
    elif frame["place"] == "":
        return "ask-place"
    elif frame["date"] == "":
        return "ask-date"
    elif frame["type"] == "":
        return "ask-type"
    else:
        return "tell-info"

# フレーム
frame = {"place": "", "date": "", "type": ""}

print("sys> こちらは天気情報案内システムです")
print("sys> ご用件をどうぞ")

while True:
    text = input("> ")

    # 現在のフレームを表示
    print(f"frame= {frame}")

    da, conceptdict = da_concept.process(text)

    frame = update_frame(frame, da, conceptdict)

    print(f"frame= {frame}")

    sys_da = next_system_da(frame)

    print(sys_da)
    if sys_da == "tell-info":
        print("天気情報をお伝えします")
        break
    else:
        sysutt = uttdic[sys_da]
        print("SYS>", sysutt)

print("ご利用ありがとうございました")