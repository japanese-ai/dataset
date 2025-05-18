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
  "質問": "なぜPhoto CDはすべてのコンピュータで動作しないのですか？",
  "参考情報": "Photo CDはKodakによって設計され、高品質の画像をCDにデジタル化して保存するシステムです。このシステムでは、専用のKodak機器を使用して画像を印刷することもできます。",
  "誤答候補": "特別なKodak機器",
  "答え": "<p>Photo CDは、<strong>特別なKodak機器</strong>が必要なため、すべてのコンピュータで動作しません。📄 ✅</p><ul><li>Photo CDは専用のソフトウェアやハードウェアで再生できます。</li><li>これにより、画像を印刷したり、高画質で閲覧したりできます。</li><li>そのため、一般的なコンピュータでは再生できません。</li></ul><p>まとめ：Photo CDは、<strong>特別なKodak機器</strong>が必要です。✅</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "Photo_CD", "label": "Photo CD", "name": "Photo CD" },
      { "id": "Kodak_Machine", "label": "Kodak機器", "name": "Kodak機器" }
    ],
    "関係": [
      { "source": "Photo_CD", "relation": "requires", "target": "Kodak_Machine" }
    ]
  }
}
{
  "質問": "Kodak Picture CDはいつ発売されましたか？",
  "参考情報": "Photo CDはKodakによって設計され、高品質の画像をCDにデジタル化して保存するシステムです。Kodak Picture CDは、消費者向けのCD-ROM形式の製品です。",
  "誤答候補": "1992年",
  "答え": "<p>Kodak Picture CDは<strong>1992年</strong>に発売されました。📄 ✅</p><ul><li>Kodak Picture CDは、消費者向けのCD-ROM形式の製品です。</li><li>これは、普通のコンピュータで再生でき、写真を保存する目的で設計されました。</li><li>Photo CDは高品質の画像を保存するシステムであり、別の製品です。</li></ul><p>まとめ：Kodak Picture CDは<strong>1992年</strong>に発売されました。✅</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "Kodak_Picture_CD", "label": "Kodak Picture CD", "name": "Kodak Picture CD" }
    ],
    "関係": [
      { "source": "Kodak_Picture_CD", "relation": "released_in", "target": "1992" }
    ]
  }
}
{
  "質問": "Red Bookの「アンチコピー」サブコードはいつ書かれたのですか？",
  "参考情報": "Red Bookオーディオ仕様は、サブコード内に簡単な「アンチコピー」声明を含んでいますが、コピー保護機構は含まれていません。2001年頃から、レコード会社は「コピー保護された」非標準コンパクトディスクを市場に出そうとしました。",
  "誤答候補": "2001年",
  "答え": "<p>Red Bookの「アンチコピー」サブコードは<strong>2001年</strong>に書かれました。📄 ✅</p><ul><li>コピー保護されたディスクは、Red Book仕様に違反しているため、Compact Disc Digital Audioロゴを付けることはできません。</li><li>コピー保護されたディスクの多くは、コンピュータのCD-ROMドライブや一部のCDプレーヤーで再生できません。</li><li>これらのコピー保護技術に対抗するため、無料のソフトウェアが利用可能です。</li></ul><p>まとめ：Red Bookの「アンチコピー」サブコードは<strong>2001年</strong>に書かれました。✅</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "Anti_Copy_Subcode", "label": "アンチコピーサブコード", "name": "アンチコピーサブコード" }
    ],
    "関係": [
      { "source": "Anti_Copy_Subcode", "relation": "written_in", "target": "2001" }
    ]
  }
}
{
  "質問": "コピー保護システムソフトウェアを作成したのは誰ですか？",
  "参考情報": "Red Bookオーディオ仕様は、サブコード内に簡単な「アンチコピー」声明を含んでいます。これにより、コピー保護されたディスクが作成されました。これらのディスクは、コンピュータやCDプレーヤーで再生できない場合があります。",
  "誤答候補": "Philips",
  "答え": "<p>コピー保護システムソフトウェアは<strong>Philips</strong>によって作成されました。📄 ✅</p><ul><li>Philipsは、Red Book仕様に従って、コピー保護システムを開発しました。</li><li>これにより、コピー防止の技術が搭載されました。</li><li>多くのフリーソフトウェアがこれらの保護技術に対抗しています。</li></ul><p>まとめ：コピー保護システムソフトウェアは<strong>Philips</strong>によって作成されました。✅</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "Anti_Copy_Software", "label": "コピー保護システムソフトウェア", "name": "コピー保護システムソフトウェア" }
    ],
    "関係": [
      { "source": "Anti_Copy_Software", "relation": "created_by", "target": "Philips" }
    ]
  }
}
{
  "質問": "Compact Disc Digital Audioロゴはいつ著作権が取得されたのですか？",
  "参考情報": "Red Bookオーディオ仕様は、サブコード内に簡単な「アンチコピー」声明を含んでいます。これにより、コピー保護されたディスクが作成されました。多くのコピー保護されたディスクは、コンピュータやCDプレーヤーで再生できません。",
  "誤答候補": "2001年",
  "答え": "<p>Compact Disc Digital Audioロゴは<strong>2001年</strong>に著作権が取得されました。📄 ✅</p><ul><li>このロゴは、Red Book仕様に従って、コピー保護されたディスクを認識するために使用されます。</li><li>このロゴを付けることで、コピー保護されたディスクが標準仕様に従っていることが確認されます。</li><li>著作権は、コピー保護技術と関連しています。</li></ul><p>まとめ：Compact Disc Digital Audioロゴは<strong>2001年</strong>に著作権が取得されました。✅</p>",
  "グラフ情報": {
    "ノード": [
      { "id": "CD_Digital_Audio_Logo", "label": "CD Digital Audioロゴ", "name": "CD Digital Audioロゴ" }
    ],
    "関係": [
      { "source": "CD_Digital_Audio_Logo", "relation": "copyrighted_in", "target": "2001" }
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
