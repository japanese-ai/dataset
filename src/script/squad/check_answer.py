from script.squad.answer import Answer

check_data = """
{"質問": "人種が社会的構築物であるという理論に対する挑戦はどこで発表されましたか？", "参考情報": "人種が単なる社会的構築物であるという理論は、スタンフォード大学医学部の研究者たちの研究結果によって挑戦されました。研究結果は『The American Journal of Human Genetics』に発表されました。", "答え": "<p><strong>人種が社会的構築物であるという理論</strong>に対する挑戦は「<strong>The American Journal of Human Genetics</strong>」に発表されました。📖</p><p>スタンフォード大学医学部の研究者たちは、遺伝的構造と自己認識した人種/民族との相関関係を調べ、その結果を発表しました。🔬</p><p>✅この研究は、社会的な人種の概念に対する見方に疑問を投げかけました。</p>", "グラフ情報": {"ノード": [{"id": "Theory_Challenge", "label": "Challenge", "name": "理論への挑戦"}, {"id": "Journal_American_Human_Genetics", "label": "Journal", "name": "アメリカ人類遺伝学雑誌"}], "関係": [{"source": "Theory_Challenge", "relation": "published_in", "target": "Journal_American_Human_Genetics"}]}}

{"質問": "Neil Rischは、遺伝的構造と人々の自己説明との間で99.9%の一致を発見しましたが、それは何の自己説明についてですか？", "参考情報": "Neil Rischは、遺伝的構造と人々の自己認識（自己説明）との間に99.9%の一致があると発見しました。", "答え": "<p><strong>Neil Risch</strong>は、遺伝的構造と人々の「<strong>自己認識</strong>」との間に99.9%の一致があると発見しました。🧬</p><p>自己認識とは、人々が自分の人種や民族についてどのように認識しているかを指します。🧠</p><p>✅この一致率の高さは、人種認識と遺伝的構造の関連性が強いことを示唆しています。</p>", "グラフ情報": {"ノード": [{"id": "Neil_Risch", "label": "Researcher", "name": "Neil Risch"}, {"id": "Self_Description", "label": "Description", "name": "自己認識"}], "関係": [{"source": "Neil_Risch", "relation": "found_concordance_with", "target": "Self_Description"}]}}

{"質問": "人種以外で問題のあるカテゴリーは何ですか？", "参考情報": "人種が社会的構築物であるという理論が挑戦された際、性別も問題のあるカテゴリーとして挙げられました。", "答え": "<p><strong>人種</strong>以外で問題のあるカテゴリーとして「<strong>性別</strong>」が挙げられました。⚧️</p><p>性別については、自己認識と遺伝的マーカーの間に不一致があることがわかり、性別も分類の問題を抱えているとされています。🧬</p><p>✅この問題は、性別が社会的に構築されたカテゴリーであることを示唆しています。</p>", "グラフ情報": {"ノード": [{"id": "Category", "label": "Category", "name": "カテゴリー"}, {"id": "Sex", "label": "Category", "name": "性別"}], "関係": [{"source": "Category", "relation": "problematic_category", "target": "Sex"}]}}

{"質問": "自己認識は生物学と完全には一致しないかもしれないと言われていますが、それは何ですか？", "参考情報": "研究者たちは、自己認識が生物学とは完全に一致しないかもしれないと指摘しています。", "答え": "<p><strong>自己認識</strong>は生物学とは完全には一致しないかもしれないと言われています。🧠🔬</p><p>自己認識とは、個人が自分の人種や性別をどのように認識しているかですが、これは生物学的な現実と必ずしも一致しないことがあるとされています。⚖️</p><p>✅自己認識と生物学的な現実との不一致は、性別や人種に関する複雑な問題を浮き彫りにしています。</p>", "グラフ情報": {"ノード": [{"id": "Self_Identification", "label": "Identification", "name": "自己認識"}, {"id": "Biology", "label": "Biology", "name": "生物学"}], "関係": [{"source": "Self_Identification", "relation": "not_correlated_with", "target": "Biology"}]}}

{"質問": "どの国で人種が「生物学的に化された（Biologized）」と言われていますか？", "参考情報": "ブラジルでは人種が「生物学的に化された」と言われています。", "答え": "<p><strong>ブラジル</strong>では、人種が「<strong>生物学的に化された</strong>」と言われています。🇧🇷</p><p>ブラジルでは、遺伝的背景と表現型の違いに基づいて人種が分類され、厳格な血統規則は存在しませんでした。🧬</p><p>✅この方法では、同じ親から生まれた兄妹が異なる人種に分類されることもあります。</p>", "グラフ情報": {"ノード": [{"id": "Brazil", "label": "Country", "name": "ブラジル"}, {"id": "Biologized_Race", "label": "Concept", "name": "生物学的に化された人種"}], "関係": [{"source": "Brazil", "relation": "biologized_in", "target": "Biologized_Race"}]}}


"""

answer = Answer()
answer.have_graph_data = True

is_valid, clipboard_data = answer.check_clipboard_data(check_data, check_rows=5)
print(clipboard_data)
print(f"Is Valid: {is_valid}")
