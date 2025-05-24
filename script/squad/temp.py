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
{"質問":"血中コレステロールは何に大きな影響を与えますか？","参考情報":"文中では『食事性コレステロールは血中コレステロールに有意な影響を与えない』とされており、逆の関係を示唆する記述はない。","誤答候補":"食事性コレステロール","答え":"<p>🧪 <strong>ステップ1:</strong> 質問は「血中コレステロールは何に大きな影響を与えますか？」です。</p>\n<p>📄 <strong>ステップ2:</strong> 文中には「食事性コレステロールは血中コレステロールに有意な影響を与えない」と明記されています。</p>\n<p>🔄 <strong>ステップ3:</strong> この関係は片方向であり、血中コレステロールが食事性コレステロールに影響を与えるとは述べられていません。</p>\n<p>❌ <strong>誤答:</strong> 『食事性コレステロール』は影響を受ける側であり、与える側ではないため誤答です。</p>\n<p>✅ まとめ：血中コレステロールは<strong>食事性コレステロールに影響を与えるとはされていません</strong>。因果関係を逆に捉えないよう注意しましょう。📉🚫</p>","グラフ情報":{"ノード":[{"id":"Biomarker_BloodCholesterol","label":"Biomarker","name":"血中コレステロール"},{"id":"Substance_DietaryCholesterol","label":"Substance","name":"食事性コレステロール"}],"関係":[{"source":"Substance_DietaryCholesterol","relation":"not_significantly_affects","target":"Biomarker_BloodCholesterol"}]}}
{"質問":"どのタイプのコレステロールが注意深い制限を必要としますか？","参考情報":"文中では『食事性コレステロールは血中コレステロールに大きな影響を与えないため、制限の推奨は必要ないかもしれない』と記述されている。","誤答候補":"食事性","答え":"<p>🧂 <strong>ステップ1:</strong> 質問は「どのタイプのコレステロールが注意深い制限を必要としますか？」です。</p>\n<p>📄 <strong>ステップ2:</strong> 文中では、食事性コレステロールは血中コレステロールに大きな影響を与えないため、「その摂取に関する推奨は不要かもしれない」と述べられています。</p>\n<p>❌ <strong>誤答:</strong> 『食事性』は制限を必要としない可能性が高いため、誤答です。</p>\n<p>✅ まとめ：現在の知見では、<strong>食事性コレステロールは制限対象とは考えにくい</strong>です。🍳🔍</p>","グラフ情報":{"ノード":[{"id":"Substance_DietaryCholesterol","label":"Substance","name":"食事性コレステロール"},{"id":"Status_Restriction","label":"Status","name":"制限の必要性"}],"関係":[{"source":"Substance_DietaryCholesterol","relation":"does_not_require","target":"Status_Restriction"}]}}
{"質問":"トランス〇〇はリスクを低下させますか？","参考情報":"文中で『トランス脂肪はリスクを増加させるようである』と明記されており、リスク低下とは逆の効果である。","誤答候補":"脂肪","答え":"<p>⚠️ <strong>ステップ1:</strong> 質問は「トランス〇〇はリスクを低下させますか？」です。</p>\n<p>📄 <strong>ステップ2:</strong> 文中では『トランス脂肪はリスクを<strong>増加させる</strong>ようである』と明確に述べられています。</p>\n<p>❌ <strong>誤答:</strong> 『脂肪』は文中ではリスクを高めるとされており、リスク低下とは逆の効果です。</p>\n<p>✅ まとめ：トランス脂肪は<strong>健康リスクを増大させる</strong>ため、リスク低下に寄与するという主張は誤りです。🚫🍟</p>","グラフ情報":{"ノード":[{"id":"Substance_TransFat","label":"Substance","name":"トランス脂肪"},{"id":"Effect_HealthRisk","label":"Effect","name":"健康リスク"}],"関係":[{"source":"Substance_TransFat","relation":"increases","target":"Effect_HealthRisk"}]}}
{"質問":"心筋梗塞のリスクを減らすことが示されている遺伝子変異はいくつありますか？","参考情報":"文中では27の遺伝子変異が『リスクを増加させる』と述べられており、リスクを減らすものではない。","誤答候補":"27個","答え":"<p>🧬 <strong>ステップ1:</strong> 質問は「心筋梗塞のリスクを減らすことが示されている遺伝子変異はいくつありますか？」です。</p>\n<p>📄 <strong>ステップ2:</strong> 文中では「27の遺伝子変異が心筋梗塞（MI）のリスクを<strong>増加</strong>させる」とあります。</p>\n<p>❌ <strong>誤答:</strong> 『27個』はリスクを<strong>減らす</strong>のではなく<strong>増やす</strong>ものであり、誤った理解です。</p>\n<p>✅ まとめ：27の遺伝子変異は<strong>リスク増加</strong>に関連しており、リスク低下とは無関係です。⚠️📉</p>","グラフ情報":{"ノード":[{"id":"Disease_MI","label":"Disease","name":"心筋梗塞"},{"id":"GeneticVariant_27","label":"GeneticVariantGroup","name":"27個の遺伝子変異"},{"id":"Effect_IncreaseRisk","label":"Effect","name":"リスク増加"}],"関係":[{"source":"GeneticVariant_27","relation":"associated_with","target":"Effect_IncreaseRisk"},{"source":"Effect_IncreaseRisk","relation":"targets","target":"Disease_MI"}]}}
{"質問":"PCSK9はどの遺伝子座にありますか？","参考情報":"文中では『心筋梗塞との最も強い関連は9p21遺伝子座にある』とされているが、PCSK9がそこに含まれるとは書かれていない。他の遺伝子名の1つとして挙げられているだけである。","誤答候補":"9p21","答え":"<p>🧬 <strong>ステップ1:</strong> 質問は「PCSK9はどの遺伝子座にありますか？」です。</p>\n<p>📄 <strong>ステップ2:</strong> 文中で「最も強い関連があるのは9p21遺伝子座」としつつも、<strong>PCSK9がその中にあるとは明記されていません</strong>。</p>\n<p>❌ <strong>誤答:</strong> 『9p21』はCDKN2A・2Bの遺伝子座であり、PCSK9についての記載は他の場所にある可能性があります。</p>\n<p>✅ まとめ：PCSK9が9p21遺伝子座に属するという明確な記述はなく、断定は誤りです。🔍🚫</p>","グラフ情報":{"ノード":[{"id":"Gene_PCSK9","label":"Gene","name":"PCSK9"},{"id":"Locus_9p21","label":"Locus","name":"9p21遺伝子座"}],"関係":[{"source":"Gene_PCSK9","relation":"not_located_in","target":"Locus_9p21"}]}}

"""
clipboard_data = clipboard_data.replace("</p>\n<p>", "</p><p>")
temp_lines = clipboard_data.strip().splitlines()

patterns = [(r"\n},\n{", "\n}\n\n{"), (r"\n}\n{", "\n}\n\n{")]


def replace_with_fallback(data):
    for pattern, replacement in patterns:
        match = re.search(pattern, data, re.MULTILINE)
        if match:
            data = re.sub(pattern, replacement, data, flags=re.MULTILINE)
            break

    return data


if len(temp_lines) > 20:
    clipboard_data = replace_with_fallback(clipboard_data)
    clipboard_data = clipboard_data.strip().split("\n\n")
    clipboard_data = [json.loads(obj) for obj in clipboard_data]

    clipboard_data = [json.dumps(obj, ensure_ascii=False) for obj in clipboard_data]

    clipboard_data = "\n".join(clipboard_data)
else:
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
