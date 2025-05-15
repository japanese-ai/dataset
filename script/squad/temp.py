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
        except json.JSONDecodeError:
            return False
    return True


data = """{"質問":"2012年5月に目標を演説で述べたのは誰ですか？","参考情報":"オバマ大統領は2013年5月に、アメリカを脅かす過激派ネットワークの解体を目標とする演説を行ったと記載されています。","誤答候補":"オバマ","答え":"<p>📆 <strong>ステップ1:</strong> 質問では「2012年5月」とありますが、文中では<strong>2013年5月</strong>にオバマ大統領が目標を明言したとされています。</p>\n<p>🧾 <strong>ステップ2:</strong> よって「2012年5月」とするのは文書と一致せず、明確にサポートされていません。</p>\n<p>❌ <strong>誤答:</strong> 「オバマ」→ 人物自体は正しいが、日付が一致しないため誤答とされます。</p>\n<p>⚠️ <strong>結論:</strong> オバマは2013年に目標を述べており、2012年ではありません。</p>\n<p>まとめ文：「<strong>オバマ大統領</strong>」が目標を述べたのは<strong>2013年5月</strong>であり、「2012年5月」ではないため、この答えは<strong>誤り</strong>です。❌</p>","グラフ情報":{"ノード":[{"id":"Barack_Obama","label":"Person","name":"バラク・オバマ"},{"id":"Speech_2013_May","label":"Speech","name":"2013年5月の演説"},{"id":"Goal_CounterExtremism","label":"Goal","name":"過激派ネットワークの解体"}],"関係":[{"source":"Barack_Obama","relation":"delivered","target":"Speech_2013_May"},{"source":"Speech_2013_May","relation":"defined_goal","target":"Goal_CounterExtremism"}]}}
{"質問":"「海外緊急作戦」が「暴力的過激主義対策」に変更されたのは何年ですか？","参考情報":"「海外緊急作戦（Overseas Contingency Operations）」という言葉は2010年に「暴力的過激主義対策（Countering Violent Extremism）」に変更されたとあります。","誤答候補":"2010年","答え":"<p>📅 <strong>ステップ1:</strong> 文中には、2010年に米国行政管理予算局が用語を変更したと明記されています。</p>\n<p>🗂 <strong>ステップ2:</strong> 「Overseas Contingency Operations」→「Countering Violent Extremism」へと変化しました。</p>\n<p>❌ <strong>誤答:</strong> 「2010年」→ 実際は正しい年ですが、形式上誤答候補となっています。</p>\n<p>✅ <strong>結論:</strong> 正確な年は<strong>2010年</strong>です。</p>\n<p>まとめ文：「<strong>海外緊急作戦</strong>」という名称は<strong>2010年</strong>に「<strong>暴力的過激主義対策</strong>」に変更されました。✅</p>","グラフ情報":{"ノード":[{"id":"OCO","label":"Term","name":"海外緊急作戦"},{"id":"CVE","label":"Term","name":"暴力的過激主義対策"}],"関係":[{"source":"OCO","relation":"renamed_to","target":"CVE"}]}}
{"質問":"2009年に「Overseas Contingency Operation」は何に改名されましたか？","参考情報":"2009年に「Global War on Terror（対テロ戦争）」から「Overseas Contingency Operation（海外緊急作戦）」へ名称が変更されたとあります。","誤答候補":"対テロ戦争","答え":"<p>🔄 <strong>ステップ1:</strong> 文中では、2009年に国防総省が「対テロ戦争」の名称を「Overseas Contingency Operation（OCO）」に変更したと述べられています。</p>\n<p>📄 <strong>ステップ2:</strong> 「Overseas Contingency Operation」は新名称であり、旧称は「対テロ戦争」です。</p>\n<p>❌ <strong>誤答:</strong> 「対テロ戦争」→ これは旧名称であり、質問は「何に改名されたか？」なので逆です。</p>\n<p>⚠️ <strong>結論:</strong> この答えは方向が逆であり、正確ではありません。</p>\n<p>まとめ文：「<strong>Overseas Contingency Operation</strong>」は2009年に「<strong>対テロ戦争</strong>」から変更された名称であり、この答えは<strong>誤り</strong>です。❌</p>","グラフ情報":{"ノード":[{"id":"Global_War_Terror","label":"Term","name":"対テロ戦争"},{"id":"OCO","label":"Term","name":"海外緊急作戦"}],"関係":[{"source":"Global_War_Terror","relation":"renamed_to","target":"OCO"}]}}
{"質問":"国防総省はその名前を何に変更しましたか？","参考情報":"国防総省（Department of Defense）は「対テロ戦争」の名称を「海外緊急作戦（Overseas Contingency Operation）」に変更したと書かれています。","誤答候補":"米国行政管理予算局","答え":"<p>🏛 <strong>ステップ1:</strong> 国防総省が変更したのは自身の名称ではなく、「作戦の名称」です。</p>\n<p>📄 <strong>ステップ2:</strong> 具体的には、「Global War on Terror（対テロ戦争）」→「Overseas Contingency Operation（OCO）」です。</p>\n<p>❌ <strong>誤答:</strong> 「米国行政管理予算局（OMB）」→ この機関は<strong>用語の変更</strong>に関わったが、国防総省の名前ではない。</p>\n<p>⚠️ <strong>結論:</strong> 国防総省が変更したのは自らの名前ではなく、作戦名です。誤答は別機関の名称で誤解を招きます。</p>\n<p>まとめ文：<strong>国防総省</strong>が変更したのは「対テロ戦争」→「<strong>海外緊急作戦</strong>」という<strong>作戦名</strong>であり、この選択肢は不適切です。❌</p>","グラフ情報":{"ノード":[{"id":"Dept_Defense","label":"Organization","name":"国防総省"},{"id":"Global_War_Terror","label":"Term","name":"対テロ戦争"},{"id":"OCO","label":"Term","name":"海外緊急作戦"}],"関係":[{"source":"Dept_Defense","relation":"renamed_term_from_to","target":["Global_War_Terror","OCO"]}]}}
{"質問":"ジェイ・ジョンソンはどの大学で働いていましたか？","参考情報":"ジェイ・ジョンソンは2012年にオックスフォード大学で講演を行ったとありますが、その大学で「働いていた」とは書かれていません。","誤答候補":"オックスフォード","答え":"<p>🏫 <strong>ステップ1:</strong> 文中では、ジェイ・ジョンソンは「2012年にオックスフォード大学で講演した」と記述されています。</p>\n<p>💼 <strong>ステップ2:</strong> 「講演した」＝「勤務していた」とは限りません。<strong>在籍情報は書かれていません</strong>。</p>\n<p>❌ <strong>誤答:</strong> 「オックスフォード」→ この大学で働いていたという記載はないため誤りです。</p>\n<p>⚠️ <strong>結論:</strong> ジョンソン氏がこの大学で職を得ていた証拠は文中にありません。</p>\n<p>まとめ文：「<strong>オックスフォード大学</strong>」で講演は行いましたが、「<strong>勤務</strong>していた」とは記されておらず、この答えは<strong>誤り</strong>です。❌</p>","グラフ情報":{"ノード":[{"id":"Jeh_Johnson","label":"Person","name":"ジェイ・ジョンソン"},{"id":"Oxford_Uni","label":"Location","name":"オックスフォード大学"},{"id":"Event_2012","label":"Event","name":"2012年の講演"}],"関係":[{"source":"Jeh_Johnson","relation":"gave_speech_at","target":"Event_2012"},{"source":"Event_2012","relation":"held_at","target":"Oxford_Uni"}]}}
"""
clipboard_data = "\n".join([line for line in data.split("\n") if line.strip()])
clipboard_data += "\n"
lines = clipboard_data.strip().splitlines()

print(is_jsonl(lines))
