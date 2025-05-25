from script.squad.plausible_answer import PlausibleAnswer

check_data = """
{"no": 42419, "質問": "メキシコサボテンはサン・バルテルミー島に何年に持ち込まれましたか？", "参考情報": "黄色のウチワサボテンは1773年にイギリス軍の侵入に対するバリケードとして植えられたとあり、メキシコサボテンもその文脈で記されていますが、具体的に同じ年とは記載されていません。", "誤答候補": "1773年", "答え": "<p>🌵質問は<strong>メキシコサボテンがいつ持ち込まれたか</strong>についてです。</p><p>📄参考情報には、「1773年に黄色のウチワサボテンが植えられた」とありますが、<strong>メキシコサボテンについては年の明記がありません</strong>。</p><p>❌そのため、「1773年」は誤答となります。</p><p>⚠️推測できそうですが、正確な年が記載されていない以上、根拠としては不十分です。</p><p>まとめ：メキシコサボテンが持ち込まれた年は記載がなく、「1773年」は誤答です。❌</p>", "グラフ情報": {"ノード": [{"id": "Plant_MexicanCactus", "label": "Plant", "name": "メキシコサボテン"}, {"id": "Event_UnknownImport", "label": "Event", "name": "持ち込み時期不明"}], "関係": [{"source": "Plant_MexicanCactus", "relation": "was_introduced_in", "target": "Event_UnknownImport"}]}}
{"no": 42423, "質問": "ネズミイルカの寿命は通常どのくらいですか？", "参考情報": "ネズミイルカは言及されていますが、寿命についての情報は提供されていません。", "誤答候補": "50年", "答え": "<p>🐬質問は<strong>ネズミイルカの寿命</strong>に関するものです。</p><p>📄参考情報では、ネズミイルカは他の海洋哺乳類と共に言及されていますが、<strong>寿命に関する記述は存在しません</strong>。</p><p>❌「50年」という寿命は一見妥当そうですが、文書には根拠がなく、<strong>誤答</strong>です。</p><p>まとめ：ネズミイルカの寿命については記載がなく、「50年」という答えは文書では支持されません。❌</p>", "グラフ情報": {"ノード": [{"id": "Species_Porpoise", "label": "Animal", "name": "ネズミイルカ"}, {"id": "Property_LifespanUnknown", "label": "Property", "name": "寿命不明"}], "関係": [{"source": "Species_Porpoise", "relation": "has_property", "target": "Property_LifespanUnknown"}]}}

"""

plausible = PlausibleAnswer()
plausible.have_graph_data = True

is_valid, clipboard_data = plausible.check_clipboard_data(check_data, check_rows=2)
print(clipboard_data)
print(f"Is Valid: {is_valid}")
