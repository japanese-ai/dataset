import json

# Your input JSON string
data = """
[
  {
    "質問": "Musée d'art moderne et contemporainはいつ完成しましたか？",
    "参考情報": "Musée d'art moderne et contemporainは、1871年以降の国際的な美術（絵画、彫刻、グラフィックアート）や装飾芸術を展示しています。",
    "誤答候補": "1871年",
    "答え": "<p><strong>Musée d'art moderne et contemporain</strong>の完成年に関する情報は明確に示されていません😊</p><p>1871年は装飾芸術の展示期間に関連しているため、完成年とは異なります❌</p><p><strong>まとめ：</strong>Musée d'art moderne et contemporainの完成年は不明ですが、1871年は誤りです✅</p>",
    "グラフ情報": {
      "ノード": [
        { "id": "Museum_ModernArt", "label": "Museum", "name": "現代美術館" },
        { "id": "Year_1871", "label": "Year", "name": "1871年" }
      ],
      "関係": [
        { "source": "Museum_ModernArt", "relation": "features_art_since", "target": "Year_1871" }
      ]
    }
  },
  {
    "質問": "Musée des Beaux-Artsの建物はどのスタイルですか？",
    "参考情報": "Musée des Beaux-Artsは、1681年から1871年の間のドイツのライン地方を中心とした古典的な美術作品を展示しています。",
    "誤答候補": "ゲルマン様式",
    "答え": "<p><strong>Musée des Beaux-Arts</strong>の建物は、特定のスタイルに関する詳細な情報は提供されていません😊</p><p>ゲルマン様式は、展示されている美術作品の期間に関連しているため、建物のスタイルとは直接関係ありません❌</p><p><strong>まとめ：</strong>Musée des Beaux-Artsの建物のスタイルについては明確な記述はありません✅</p>",
    "グラフ情報": {
      "ノード": [
        { "id": "Museum_BeauxArts", "label": "Museum", "name": "美術館" },
        { "id": "Style_Germanic", "label": "Style", "name": "ゲルマン様式" }
      ],
      "関係": [
        { "source": "Museum_BeauxArts", "relation": "features_art_period", "target": "Style_Germanic" }
      ]
    }
  },
  {
    "質問": "Musée des arts décoratifsは何年に完成しましたか？",
    "参考情報": "Musée des arts décoratifsは、1681年から1871年の間のフランス様式の装飾芸術を展示しています。",
    "誤答候補": "1871年",
    "答え": "<p><strong>Musée des arts décoratifs</strong>の完成年に関する具体的な情報は提供されていません😊</p><p>1871年は展示されている装飾芸術の期間に関連しているため、完成年とは関係ありません❌</p><p><strong>まとめ：</strong>Musée des arts décoratifsの完成年は明確に記載されていないため、1871年は誤りです✅</p>",
    "グラフ情報": {
      "ノード": [
        { "id": "Museum_ArtsDecoratifs", "label": "Museum", "name": "装飾美術館" },
        { "id": "Year_1871", "label": "Year", "name": "1871年" }
      ],
      "関係": [
        { "source": "Museum_ArtsDecoratifs", "relation": "features_art_period", "target": "Year_1871" }
      ]
    }
  },
  {
    "質問": "Musée des arts décoratifsの建物はどのスタイルですか？",
    "参考情報": "Musée des arts décoratifsは、1681年から1871年のフランス様式の装飾芸術を展示しています。",
    "誤答候補": "ゲルマン様式",
    "答え": "<p><strong>Musée des arts décoratifs</strong>の建物は、フランス様式に関連する展示内容に基づいています😊</p><p>したがって、ゲルマン様式という誤った情報は不正確です❌</p><p><strong>まとめ：</strong>Musée des arts décoratifsの建物はフランス様式に関連しています✅</p>",
    "グラフ情報": {
      "ノード": [
        { "id": "Museum_ArtsDecoratifs", "label": "Museum", "name": "装飾美術館" },
        { "id": "Style_French", "label": "Style", "name": "フランス様式" }
      ],
      "関係": [
        { "source": "Museum_ArtsDecoratifs", "relation": "features_style", "target": "Style_French" }
      ]
    }
  },
  {
    "質問": "1683年以前、ストラスブールは誰が支配していましたか？",
    "参考情報": "ストラスブールは1683年にフランス王国に併合される前、神聖ローマ帝国とドイツ語圏の知的世界に深く関わりがありました。",
    "誤答候補": "フランス王国",
    "答え": "<p><strong>ストラスブール</strong>は1683年以前、神聖ローマ帝国の一部であり、ドイツ語圏の知的世界と密接に関連していました😊</p><p>したがって、フランス王国による支配は1683年以降です❌</p><p><strong>まとめ：</strong>ストラスブールは1683年以前、フランス王国ではなく神聖ローマ帝国が支配していました✅</p>",
    "グラフ情報": {
      "ノード": [
        { "id": "Strasbourg", "label": "City", "name": "ストラスブール" },
        { "id": "Empire_HolyRoman", "label": "Empire", "name": "神聖ローマ帝国" }
      ],
      "関係": [
        { "source": "Strasbourg", "relation": "controlled_by", "target": "Empire_HolyRoman" }
      ]
    }
  }
]
"""

# Convert JSON string to Python object
data_list = json.loads(data)

# Convert each dictionary into a single-line JSON
json_lines = [json.dumps(entry, ensure_ascii=False) for entry in data_list]

# Output each JSON object in a single line
print("\n".join(json_lines) + "\n")
