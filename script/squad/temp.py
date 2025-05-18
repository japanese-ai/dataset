import json


def is_valid_graph_info(graph_info):
    if not isinstance(graph_info, dict):
        return False

    if not all(key in graph_info for key in ["ノード", "関係"]):
        return False

    if not isinstance(graph_info["ノード"], list):
        return False
    for node in graph_info["ノード"]:
        if not isinstance(node, dict):
            return False
        if not all(key in node for key in ["id", "label", "name"]):
            return False
        if not all(isinstance(node[key], str) for key in ["id", "label", "name"]):
            return False

    if not isinstance(graph_info["関係"], list):
        return False
    for relation in graph_info["関係"]:
        if not isinstance(relation, dict):
            return False
        if not all(key in relation for key in ["source", "relation", "target"]):
            return False
        if not all(
            isinstance(relation[key], str) for key in ["source", "relation", "target"]
        ):
            return False

    return True


def is_valid_format(obj):
    required_keys = {"質問", "参考情報", "誤答候補", "答え"}

    if not isinstance(obj, dict):
        return False

    if not required_keys.issubset(obj.keys()):
        return False
    if not all(isinstance(obj[key], str) for key in required_keys):
        return False

    if "グラフ情報" not in obj:
        return False
    if not is_valid_graph_info(obj["グラフ情報"]):
        return False

    return True


def is_jsonl(lines):
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if not is_valid_format(obj):
                print(f"Invalid format in line {i}: {line}")
                return False
        except json.JSONDecodeError as e:
            print(e)
            return False
    return True


clipboard_data = """
{
  "質問": "チャールストンの市内で記録された最も低い温度は何度ですか？",
  "参考情報": "チャールストンの市内で記録された最も高い温度は1985年6月2日と1944年6月24日に104°F（40°C）で、最も低い温度は1899年2月14日に7°F（−14°C）でした。空港では、公式記録が保持されており、1999年8月1日に105°F（41°C）から1985年1月21日に6°F（−14°C）までの歴史的な範囲があります。ハリケーンは夏と初秋にこの地域にとって大きな脅威です。",
  "誤答候補": "104°F",
  "答え": "<p><strong>チャールストン市内で記録された最も低い温度は<strong>7°F（−14°C）</strong>です。🌨️</p><p><strong>理由</strong>: この温度は1899年2月14日に記録され、最も低い気温です。📄</p><p><strong>なぜ7°Fだったのか？</strong>: 冷たい冬の一環として、1899年に記録されました。✅</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "Charleston_Low_Temperature", "label": "Temperature", "name": "7°F（−14°C）" },
      { "id": "City_Charleston", "label": "City", "name": "チャールストン" }
    ],
    "関係": [
      { "source": "City_Charleston", "relation": "has_lowest_temperature_of", "target": "Charleston_Low_Temperature" }
    ]
  }
}

{
  "質問": "チャールストンの夏と初秋において、軽度な脅威となる嵐の種類は何ですか？",
  "参考情報": "チャールストンは湿潤亜熱帯気候（ケッペン気候分類Cfa）で、夏と初秋においてハリケーンが主な脅威となります。特に、1989年9月21日に発生したハリケーン・ヒューゴはカテゴリー4の嵐でした。夏の間、降水量は雷雨という形で降り、湿度も高くなります。",
  "誤答候補": "ハリケーン",
  "答え": "<p><strong>チャールストンの夏と初秋において軽度な脅威となる嵐の種類は<strong>ハリケーン</strong>です。🌪️</p><p><strong>理由</strong>: ハリケーンはこの地域でよく発生し、特に1989年のハリケーン・ヒューゴは大きな影響を与えました。📄</p><p><strong>なぜハリケーンが脅威となるのか？</strong>: 夏と初秋に発生することが多く、巨大な影響を与えるためです。✅</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "Charleston_Threat_Storm", "label": "Storm", "name": "ハリケーン" },
      { "id": "Season_Summer_Fall", "label": "Season", "name": "夏と初秋" }
    ],
    "関係": [
      { "source": "Season_Summer_Fall", "relation": "experiences", "target": "Charleston_Threat_Storm" }
    ]
  }
}

{
  "質問": "チャールストンで1998年に発生したハリケーンは何ですか？",
  "参考情報": "チャールストンの最も著名なハリケーンの1つは1989年9月21日に発生したハリケーン・ヒューゴです。このカテゴリー4の嵐は市内に大きな影響を与えました。1998年に発生したハリケーンは記録されていません。",
  "誤答候補": "ハリケーン・ヒューゴ",
  "答え": "<p><strong>1998年にチャールストンで発生したハリケーンは<strong>記録されていません</strong>。⚠️</p><p><strong>理由</strong>: 1998年に特定のハリケーンが記録されていないためです。📄</p><p><strong>なぜ1998年にハリケーンが発生しなかったのか？</strong>: 1998年は特定の影響を与えるハリケーンが発生しませんでした。✅</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "Hurricane_Hugo", "label": "Hurricane", "name": "ハリケーン・ヒューゴ" },
      { "id": "Year_1998", "label": "Year", "name": "1998年" }
    ],
    "関係": [
      { "source": "Year_1998", "relation": "had_no_hurricane_in", "target": "Hurricane_Hugo" }
    ]
  }
}

{
  "質問": "チャールストンの市内で記録された最も高い温度は何度ですか？",
  "参考情報": "チャールストンの市内で記録された最も高い温度は、1985年6月2日と1944年6月24日に104°F（40°C）でした。空港では公式記録が保持されており、1999年8月1日に105°F（41°C）に達したことがあります。",
  "誤答候補": "7°F（−14°C）",
  "答え": "<p><strong>チャールストンの市内で記録された最も高い温度は<strong>104°F（40°C）</strong>です。🌞</p><p><strong>理由</strong>: 104°F（40°C）は1985年6月2日と1944年6月24日に記録され、最も高い気温となっています。📄</p><p><strong>なぜ104°Fだったのか？</strong>: これがチャールストンで記録された最も高い気温です。✅</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "Charleston_High_Temperature", "label": "Temperature", "name": "104°F（40°C）" },
      { "id": "City_Charleston", "label": "City", "name": "チャールストン" }
    ],
    "関係": [
      { "source": "City_Charleston", "relation": "has_highest_temperature_of", "target": "Charleston_High_Temperature" }
    ]
  }
}

{
  "質問": "チャールストンの空港で1999年8月1日に記録された最も暖かい日付はいつですか？",
  "参考情報": "チャールストンの空港では、1999年8月1日に記録的な105°F（41°C）が記録されました。この日が空港での最も暖かい日とされています。",
  "誤答候補": "1985年1月21日",
  "答え": "<p><strong>チャールストンの空港で1999年8月1日に記録された最も暖かい日付は<strong>1999年8月1日</strong>です。🌡️</p><p><strong>理由</strong>: 1999年8月1日が空港で最も高い気温が記録された日です。📄</p><p><strong>なぜ1999年8月1日なのか？</strong>: 空港で最も高い気温の記録として残っているからです。✅</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "Date_1999_08_01", "label": "Date", "name": "1999年8月1日" },
      { "id": "Charleston_Airport", "label": "Location", "name": "チャールストン空港" }
    ],
    "関係": [
      { "source": "Charleston_Airport", "relation": "recorded_highest_temperature_on", "target": "Date_1999_08_01" }
    ]
  }
}

"""
temp_lines = clipboard_data.strip().splitlines()

if len(temp_lines) > 10:
    clipboard_data = clipboard_data.strip().replace("\n},\n{", "\n}\n\n{")
    clipboard_data = clipboard_data.strip().split("\n\n")
    clipboard_data = [json.loads(obj) for obj in clipboard_data]

    clipboard_data = [json.dumps(obj, ensure_ascii=False) for obj in clipboard_data]

    clipboard_data = "\n".join(clipboard_data)
else:
    clipboard_data = clipboard_data.replace("</p>\n<p>", "</p><p>")
    clipboard_data = [
        line
        for line in clipboard_data.strip().splitlines()
        if line not in ["", "}", ",", "},"]
    ]
    clipboard_data = [
        (
            line.strip() + ("}" if line.strip().endswith("}]}") else "")
            if not line.endswith("}]}}")
            else line
        )
        for line in clipboard_data
    ]
    clipboard_data = [(line.replace("}]}},", "}]}}")) for line in clipboard_data]
    clipboard_data = "\n".join(clipboard_data)

clipboard_data += "\n"
print(clipboard_data)

lines = clipboard_data.strip().splitlines()

print(is_jsonl(lines))
