from script.squad.plausible_answer import PlausibleAnswer

check_data = """
{"no":23332,"質問":"ストラスブール大聖堂はいつ建てられましたか？","参考情報":"文書では、1524年から1681年の間、ストラスブール大聖堂がルター派の教会であったことが記載されていますが、建設年は明記されていません。","誤答候補":"1524","答え":"<p>🏰 <strong>ステップ1：</strong> ストラスブール大聖堂の<strong>建設年</strong>を尋ねる質問です。</p><p>📄 <strong>ステップ2：</strong> 文中では「1524年から1681年にかけてルター派であった」とのみ書かれており、これは宗教的利用の期間を示しています。</p><p>⚠️ <strong>ステップ3：</strong>「1524年に建てられた」という主張は、宗教利用の開始年と建設年を混同している誤答です。</p><p>❌ plausible answer: 1524 → <strong>建設年の記述は文書に無く、1524年は宗教使用の開始年です</strong>。</p><p>📚 引用：「was Lutheran from 1524 to 1681」</p><p>まとめ文：ストラスブール大聖堂の<strong>建設年は文書に記載されておらず</strong>、「1524年」とするのは誤りです。✅🏛️</p>","グラフ情報":{"ノード":[{"id":"Strasbourg_Cathedral","label":"建築物","name":"ストラスブール大聖堂"},{"id":"Lutheran","label":"宗派","name":"ルター派"}],"関係":[{"source":"Strasbourg_Cathedral","relation":"宗派であった","target":"Lutheran","start":"1524年","end":"1681年"}]}}
{"no":24967,"質問":"League Against Cruel Sportsは何年に設立されましたか？","参考情報":"文書では、この団体が2016年に活動したことは記載されているが、設立年についての記述はない。","誤答候補":"2016年","答え":"<p>📆 <strong>ステップ1：</strong> 質問は「League Against Cruel Sportsの設立年」です。</p><p>📄 <strong>ステップ2：</strong> 文書には、2016年にイートン校のビーグルクラブを批判したという活動があったと書かれていますが、<strong>設立年の記載はありません</strong>。</p><p>⚠️ <strong>ステップ3：</strong>「2016年」は活動年であり、設立時期ではありません。</p><p>❌ plausible answer: 2016年 → <strong>文中に設立年の記載がなく、2016年は活動が確認された年です</strong>。</p><p>📚 引用：「In 2016, the League criticized the Eton Beagle Club」</p><p>まとめ文：League Against Cruel Sportsの<strong>設立年は文書に明示されておらず</strong>、「2016年」は誤答です。✅📢🐾</p>","グラフ情報":{"ノード":[{"id":"League_Against_Cruel_Sports","label":"団体","name":"動物虐待反対リーグ"},{"id":"Eton_Beagle_Club","label":"団体","name":"イートン・ビーグルクラブ"}],"関係":[{"source":"League_Against_Cruel_Sports","relation":"批判した対象","target":"Eton_Beagle_Club","year":"2016年"}]}}
{"no":24968,"質問":"イギリスでノウサギ狩りが違法になったのは何年ですか？","参考情報":"文書では、2016年にノウサギ狩りが違法であると疑われた事件が起きたことは記載されていますが、違法化された年そのものは書かれていません。","誤答候補":"2016年","答え":"<p>🐇 <strong>ステップ1：</strong> この質問は「ノウサギ狩りが違法になった年」を問うています。</p><p>📄 <strong>ステップ2：</strong> 文中では2016年に違法狩猟の疑いがある事件があったと書かれていますが、<strong>違法化された年の記載はありません</strong>。</p><p>⚠️ <strong>ステップ3：</strong>「2016年」は事件が発生した年であって、法制化の年とは限りません。</p><p>❌ plausible answer: 2016年 → <strong>事件が起きた年であり、法律の制定年ではないため誤答です</strong>。</p><p>📚 引用：「In 2016, illegal hare hunting was suspected at Eton」</p><p>まとめ文：ノウサギ狩りが<strong>違法化された年は文書に記載されておらず</strong>、「2016年」とするのは不正確です。✅⚖️</p>","グラフ情報":{"ノード":[{"id":"UK_Hare_Hunting_Ban","label":"法律","name":"イギリスのノウサギ狩猟禁止法"},{"id":"Illegal_Hunting_Event","label":"事件","name":"2016年の違法狩猟疑惑"}],"関係":[{"source":"Illegal_Hunting_Event","relation":"関連法","target":"UK_Hare_Hunting_Ban"}]}}
{"no":24969,"質問":"イギリスでノウサギ狩りに最適な月はいつですか？","参考情報":"2016年1月に事件が起こったことは記載されていますが、その月が狩猟に最適であるとの記述はありません。","誤答候補":"1月","答え":"<p>📆 <strong>ステップ1：</strong> 質問は「ノウサギ狩りに最適な月」を問うています。</p><p>📄 <strong>ステップ2：</strong> 文書では、2016年1月に事件があったと記載されていますが、それが<strong>最適な狩猟月であるとは書かれていません</strong>。</p><p>⚠️ <strong>ステップ3：</strong> 事件が1月に起きたからといって、それを最適な時期と結論づけるのは飛躍があります。</p><p>❌ plausible answer: 1月 → <strong>事件発生日を根拠に「最適」とするのは誤解であり、文書上の裏付けがありません</strong>。</p><p>📚 引用：「A suspected illegal hunt occurred in January 2016」</p><p>まとめ文：ノウサギ狩りに最適な月は<strong>文中に記載されておらず</strong>、「1月」は誤答です。✅📉🐰</p>","グラフ情報":{"ノード":[{"id":"Hare_Hunting_Season","label":"狩猟期","name":"ノウサギ狩猟期"},{"id":"Month_January","label":"月","name":"1月"}],"関係":[{"source":"Hare_Hunting_Season","relation":"事件が起きた月","target":"Month_January"}]}}

"""

plausible = PlausibleAnswer()
plausible.have_graph_data = False

is_valid, clipboard_data, message = plausible.check_clipboard_data(
    check_data, check_rows=4
)
print(clipboard_data)
print(f"Is Valid: {is_valid}")
print(f"Message: {message}")
