from script.squad.plausible_answer import PlausibleAnswer

check_data = """
{"no":24299,"質問":"近代保守党は、1834年に何を発表して保守主義の基本原則を定義したか？","参考情報":"1834年にロバート・ピールは『タムワース宣言』を発表し、保守主義の基本原則を定義しました。","誤答候補":"タムワース宣言","答え":"<p>📘 <strong>ステップ1:</strong> 質問は「近代保守党が1834年に発表したもの」です。</p><p>📜 <strong>ステップ2:</strong> 参考情報では、ロバート・ピールが1834年に『<strong>タムワース宣言</strong>』を発表したとされています。</p><p>🧠 <strong>ステップ3:</strong> この文書では、保守主義の原則として、漸進的改革と伝統の維持が強調されました。</p><p>❌ <strong>誤答候補:</strong> 「タムワース宣言」は本文に明記されている正解です。</p><p>まとめ：1834年に発表されたタムワース宣言が、近代保守主義の基本的理念を定義しました。✅📜🏛️</p>","グラフ情報":{"ノード":[{"id":"Tamworth_Manifesto","label":"Political Document","name":"タムワース宣言"},{"id":"Conservative_Principles","label":"Ideology","name":"保守主義の基本原則"}],"関係":[{"source":"Tamworth_Manifesto","relation":"defined","target":"Conservative_Principles"}]}}
{"no":24300,"質問":"リベラル党が分裂した原因は何か？","参考情報":"リベラル党は政治改革を巡る内部の意見対立により分裂しました。","誤答候補":"政治改革を巡る争い","答え":"<p>⚖️ <strong>ステップ1:</strong> 質問は「リベラル党が分裂した原因」です。</p><p>📚 <strong>ステップ2:</strong> 参考情報には、改革に関する争いが原因であると明記されています。</p><p>💬 <strong>ステップ3:</strong> 政治改革を巡る意見の不一致が、党の結束を崩す結果となりました。</p><p>❌ <strong>誤答候補:</strong> 「政治改革を巡る争い」は正確な要因として本文に明記されています。</p><p>まとめ：政治改革に関する内部対立が、リベラル党の分裂を招きました。✅🔧🗳️</p>","グラフ情報":{"ノード":[{"id":"Liberal_Party","label":"Political Party","name":"リベラル党"},{"id":"Political_Reform_Disputes","label":"Cause","name":"政治改革を巡る争い"}],"関係":[{"source":"Liberal_Party","relation":"split_due_to","target":"Political_Reform_Disputes"}]}}
{"no":24301,"質問":"ウィリアム・エワート・グラッドストーンが率いた政府はなぜ崩壊したか？","参考情報":"ウィリアム・グラッドストーンの政府は、選挙結果が悪化したことによって政権が崩壊しました。","誤答候補":"選挙結果の悪化","答え":"<p>📉 <strong>ステップ1:</strong> 質問は「グラッドストーン政府が崩壊した理由」です。</p><p>🗳️ <strong>ステップ2:</strong> 参考情報によれば、「<strong>選挙結果の悪化</strong>」が崩壊の直接的な原因とされています。</p><p>📊 <strong>ステップ3:</strong> 議席の減少は、信任喪失と政策実行の停滞を引き起こしました。</p><p>❌ <strong>誤答候補:</strong> 選挙結果の悪化は本文で明確に記載された正解です。</p><p>まとめ：グラッドストーンの政権は、選挙での敗北により崩壊しました。✅📉📬</p>","グラフ情報":{"ノード":[{"id":"Gladstone_Government","label":"Government","name":"グラッドストーン政府"},{"id":"Bad_Election_Results","label":"Cause","name":"選挙結果の悪化"}],"関係":[{"source":"Gladstone_Government","relation":"collapsed_due_to","target":"Bad_Election_Results"}]}}
{"no":24302,"質問":"ピット派トーリー党は、ダック・オブ・ウェリントンの政府が崩壊した後、何を始めたか？","参考情報":"ウェリントン公の政府崩壊後、ピールらピット派トーリー党は、新たな政治勢力の結集を試みました。","誤答候補":"新しい勢力の結集","答え":"<p>🔄 <strong>ステップ1:</strong> 質問は「政府崩壊後にピット派トーリー党が行った行動」です。</p><p>📖 <strong>ステップ2:</strong> 参考情報では「新しい勢力の結集」を始めたと述べられています。</p><p>🧱 <strong>ステップ3:</strong> これは後の保守党形成の基盤となる動きでした。</p><p>❌ <strong>誤答候補:</strong> 「新しい勢力の結集」は本文と一致しており、誤答ではありません。</p><p>まとめ：ピット派トーリー党は、新勢力の結集によって再編を図りました。✅🧩🤝</p>","グラフ情報":{"ノード":[{"id":"Pittite_Tories","label":"Political Group","name":"ピット派トーリー党"},{"id":"New_Coalition_Formation","label":"Action","name":"新しい勢力の結集"}],"関係":[{"source":"Pittite_Tories","relation":"started","target":"New_Coalition_Formation"}]}}
{"no":24303,"質問":"ロバート・ピールがタムワース宣言を発表した年は？","参考情報":"ロバート・ピールは1834年にタムワース宣言を発表しました。これは保守主義の立場を明確にする政治的文書でした。","誤答候補":"1834年","答え":"<p>📅 <strong>ステップ1:</strong> 質問は「タムワース宣言の発表年」です。</p><p>📘 <strong>ステップ2:</strong> 参考情報ではロバート・ピールが<strong>1834年</strong>にこれを発表したとあります。</p><p>🔍 <strong>ステップ3:</strong> この年は、保守主義が制度として明確化された重要な転換点となりました。</p><p>❌ <strong>誤答候補:</strong> 「1834年」は正しい情報です。</p><p>まとめ：ロバート・ピールは1834年にタムワース宣言を発表し、近代保守党の思想基盤を築きました。✅📖🗓️</p>","グラフ情報":{"ノード":[{"id":"Tamworth_Manifesto","label":"Political Document","name":"タムワース宣言"},{"id":"1834","label":"Year","name":"1834年"}],"関係":[{"source":"Tamworth_Manifesto","relation":"issued_in","target":"1834"}]}}

"""

plausible = PlausibleAnswer()
plausible.have_graph_data = False

is_valid, clipboard_data, message = plausible.check_clipboard_data(
    check_data, check_rows=5
)
print(clipboard_data)
print(f"Is Valid: {is_valid}")
print(f"Message: {message}")
