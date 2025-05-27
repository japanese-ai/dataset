from script.squad.plausible_answer import PlausibleAnswer

check_data = """
{"no": 38448, "質問": "酵素を説明するための略語として使われるのは何ですか？", "参考情報": "NDM-1は、広範囲のベータラクタム抗生物質に対して細菌が耐性を示す新たに発見された酵素であり、これにより耐性細菌が生じています。", "誤答候補": "TB", "答え": "<p>🧪 酵素を説明するための略語は<strong>NDM-1</strong>です。✅</p><p>📄 ステップ1: NDM-1（New Delhi Metallo-beta-lactamase-1）は、酵素の名称を短縮した略語です。</p><p>📄 ステップ2: この酵素は、細菌がベータラクタム系抗生物質に対して耐性を示す原因になります。</p><p>⚠️ ステップ3: 一方、<strong>TB</strong>（結核）は病名の略であり、酵素名とは無関係です。❌</p><p>✅ ステップ4: よって、酵素を説明する略語として正しいのは<strong>NDM-1</strong>です。</p><p>まとめ文: NDM-1は強力な抗生物質耐性を引き起こす酵素の名称であり、酵素に関する略語として使われます。✅</p>", "グラフ情報": {"ノード": [{"id": "NDM_1", "label": "酵素名略語", "name": "NDM-1"}, {"id": "Antibiotic_Resistance", "label": "耐性", "name": "抗生物質耐性"}], "関係": [{"source": "NDM_1", "relation": "説明する", "target": "Antibiotic_Resistance"}]}}
{"no": 38449, "質問": "細菌が耐性を示す新たな酵素は何ですか？", "参考情報": "NDM-1は、広範囲のベータラクタム抗生物質に対して細菌が耐性を示す新たに発見された酵素です。", "誤答候補": "ペニシリン", "答え": "<p>🧬 細菌が耐性を示す新たな酵素は<strong>NDM-1</strong>です。✅</p><p>📄 ステップ1: NDM-1は、カルバペネムなどのベータラクタム系抗生物質を分解してしまう酵素です。</p><p>📄 ステップ2: そのため、従来の治療が効かない耐性菌（例: CRE）が出現する原因になります。</p><p>⚠️ ステップ3: <strong>ペニシリン</strong>は抗生物質であり、酵素の名称ではありません。❌</p><p>✅ ステップ4: よって、正解は<strong>NDM-1</strong>です。</p><p>まとめ文: NDM-1は細菌が多くの抗生物質に耐性を持つようになる主要な新規酵素です。✅</p>", "グラフ情報": {"ノード": [{"id": "NDM_1_Enzyme", "label": "新しい酵素", "name": "NDM-1"}, {"id": "Beta_Lactam_Antibiotics", "label": "抗生物質", "name": "ベータラクタム系抗生物質"}], "関係": [{"source": "NDM_1_Enzyme", "relation": "耐性を与える", "target": "Beta_Lactam_Antibiotics"}]}}
{"no": 38450, "質問": "抗生物質の誤った使用はどのような結果をもたらしますか？", "参考情報": "抗生物質の誤った使用や過剰使用は、抗生物質耐性細菌の出現に貢献しており、自己処方などが誤使用の一例です。", "誤答候補": "治療薬の適切な使用", "答え": "<p>💊 抗生物質の誤った使用は<strong>抗生物質耐性細菌の出現</strong>を引き起こします。✅</p><p>📄 ステップ1: 誤用（例: 自己判断での服用、短期での中止）は細菌を完全に殺しきれず、耐性株を生き残らせます。</p><p>📄 ステップ2: その結果、既存の治療法では効かない細菌が発生しやすくなります。</p><p>⚠️ ステップ3: 「治療薬の適切な使用」はむしろ耐性を防ぐために重要な行為です。❌</p><p>✅ ステップ4: よって、正解は<strong>抗生物質耐性細菌の出現</strong>です。</p><p>まとめ文: 抗生物質の誤用や過剰使用は、薬が効かない細菌の増加を招き、公衆衛生に深刻な影響を与えます。✅</p>", "グラフ情報": {"ノード": [{"id": "Antibiotic_Misuse", "label": "誤用", "name": "抗生物質の誤用"}, {"id": "Resistant_Bacteria", "label": "耐性細菌", "name": "抗生物質耐性細菌"}], "関係": [{"source": "Antibiotic_Misuse", "relation": "引き起こす", "target": "Resistant_Bacteria"}]}}

"""

plausible = PlausibleAnswer()
plausible.have_graph_data = False

is_valid, clipboard_data, message = plausible.check_clipboard_data(
    check_data, check_rows=3
)
print(clipboard_data)
print(f"Is Valid: {is_valid}")
print(f"Message: {message}")
