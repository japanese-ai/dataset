import json
import re


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
    required_keys = {"質問", "参考情報", "答え"}

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
  "質問": "壊血病を防ぐのに効果があるとされた果物のジュースは何ですか？",
  "参考情報": "ジェームズ・リンドはライムジュースが長期間航海していた船乗りの壊血病を防ぐことを発見しました。",
  "答え": "<p>💡<strong>ステップ1：</strong> 壊血病とはビタミンC不足による出血性の病気です。🩸</p><p>🔬<strong>ステップ2：</strong> 1747年、イギリス海軍の医師<strong>ジェームズ・リンド</strong>が、ライムジュースが壊血病を予防する効果を発見しました。🍋</p><p>📜<strong>ステップ3：</strong> この発見は当初は無視されましたが、後にイギリスの船員は「ライミー（limeys）」と呼ばれるようになります。⚓️</p><p>✅まとめ：壊血病の予防に有効だったのは<strong>ライム</strong>のジュースでした。</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "Lime_Juice", "label": "Substance", "name": "ライムジュース" },
      { "id": "Scurvy", "label": "Disease", "name": "壊血病" }
    ],
    "関係": [
      { "source": "Lime_Juice", "relation": "prevents", "target": "Scurvy" }
    ]
  }
}
{
  "質問": "1500年から1800年の間に壊血病で亡くなった船員の数は？",
  "参考情報": "1500年から1800年の間に約200万人の船員が壊血病で死亡しました。",
  "答え": "<p>📊<strong>ステップ1：</strong> 壊血病はビタミンC不足により、長期間の航海中に多くの船員を襲った病気です。🚢</p><p>📅<strong>ステップ2：</strong> 1500年から1800年の間に、約<strong>200万人</strong>もの船員が壊血病で命を落としました。☠️</p><p>🧠<strong>ステップ3：</strong> この数字は壊血病の重大さと予防手段の重要性を物語っています。🔍</p><p>✅まとめ：壊血病により<strong>200万人</strong>が命を落としました。</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "Scurvy_Deaths", "label": "Event", "name": "壊血病による死者" }
    ],
    "関係": [
      { "source": "Scurvy_Deaths", "relation": "number", "target": "2000000" }
    ]
  }
}
{
  "質問": "イギリスの船員に付けられたあだ名は？",
  "参考情報": "発見の後、イギリスの船員は「ライミー（limeys）」と呼ばれるようになりました。",
  "答え": "<p>👨‍✈️<strong>ステップ1：</strong> ライムジュースで壊血病を予防したことから、イギリスの船員にユニークな呼び名が付きました。🍋</p><p>📣<strong>ステップ2：</strong> その呼び名は<strong>「ライミー（limeys）」</strong>です。これは彼らがライムを摂取していたことに由来します。🗣️</p><p>✅まとめ：イギリスの船員は「<strong>ライミー</strong>」と呼ばれました。</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "British_Sailors", "label": "People", "name": "イギリスの船員" },
      { "id": "Limeys", "label": "Nickname", "name": "ライミー" }
    ],
    "関係": [
      { "source": "British_Sailors", "relation": "nickname", "target": "Limeys" }
    ]
  }
}
{
  "質問": "どの栄養素が犬に与えられなかったために死亡したのか？",
  "参考情報": "タンパク質を与えなかった犬は死亡しましたが、与えられた犬は生存しました。",
  "答え": "<p>🐶<strong>ステップ1：</strong> 1816年、フランソワ・マジェンディが行った実験で、犬に炭水化物・脂肪・水のみを与えました。💧🍞🫒</p><p>☠️<strong>ステップ2：</strong> しかし<strong>タンパク質</strong>を含まない食事では犬は餓死しました。💀</p><p>🧬<strong>ステップ3：</strong> これにより、タンパク質は<strong>不可欠な栄養素</strong>であると認識されました。💪</p><p>✅まとめ：死亡の原因は<strong>タンパク質不足</strong>でした。</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "Protein", "label": "Nutrient", "name": "タンパク質" },
      { "id": "Dog_Death", "label": "Event", "name": "犬の死亡" }
    ],
    "関係": [
      { "source": "Dog_Death", "relation": "caused_by_lack_of", "target": "Protein" }
    ]
  }
}
{
  "質問": "食品を最初にカテゴリー分けした人物は誰ですか？",
  "参考情報": "ウィリアム・プラウトは1827年に食品を炭水化物・脂肪・タンパク質に分類した最初の人物でした。",
  "答え": "<p>📚<strong>ステップ1：</strong> 食品の栄養素を分類することは、現代の栄養学の基本です。🍽️</p><p>👨‍🔬<strong>ステップ2：</strong> 1827年に<strong>ウィリアム・プラウト</strong>が食品を<strong>炭水化物・脂肪・タンパク質</strong>に分けました。🧪</p><p>🧠<strong>ステップ3：</strong> これが後の栄養分類と栄養バランス理論の礎となりました。📊</p><p>✅まとめ：食品を最初にカテゴリー化したのは<strong>ウィリアム・プラウト</strong>でした。</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "William_Prout", "label": "Person", "name": "ウィリアム・プラウト" },
      { "id": "Nutrient_Categories", "label": "Concept", "name": "栄養分類（炭水化物・脂肪・タンパク質）" }
    ],
    "関係": [
      { "source": "William_Prout", "relation": "categorized", "target": "Nutrient_Categories" }
    ]
  }
}

"""
temp_lines = clipboard_data.strip().splitlines()

patterns = [(r"\n},\n{", "\n}\n\n{"), (r"\n}\n{", "\n}\n\n{")]

def replace_with_fallback(data):
  for pattern, replacement in patterns:
    match = re.search(pattern, data, re.MULTILINE)
    if match:
      data = re.sub(pattern, replacement, data, flags=re.MULTILINE)
      break

  return data

if len(temp_lines) > 10:
    clipboard_data = replace_with_fallback(clipboard_data)
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
