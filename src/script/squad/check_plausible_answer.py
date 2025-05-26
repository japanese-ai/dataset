from script.squad.plausible_answer import PlausibleAnswer

check_data = """
{"no":13154,"質問":"アメリカで最初に火あぶりの刑が行われた州はどこですか？","参考情報":"1825年にサウスカロライナ州で黒人奴隷が火あぶりにされたと記されている。","誤答候補":"サウスカロライナ州","答え":"<p>📄 本文には<strong>1825年にサウスカロライナ州</strong>で火あぶりの刑が行われた記録があります。</p><p>😊 ステップ1：この出来事は明確に記載されていますが、「最初に行われた」という記述は見当たりません。</p><p>⚠️ ステップ2：「最初」という言葉が明記されていない以上、それを前提とする誤答候補は支持されません。</p><p>❌ 理由：誤答候補「サウスカロライナ州」は火あぶりが行われた州としては正しいが、「最初に」という問いには文証がありません。</p><p>✅ まとめ：1825年に火あぶりが行われた記録はありますが、それが最初かどうかは不明です。</p>","グラフ情報":{"ノード":[
  {"id":"State_SouthCarolina","label":"State","name":"サウスカロライナ州"},
  {"id":"Event_Burning1825","label":"Event","name":"1825年の火あぶり処刑"}
],"関係":[
  {"source":"State_SouthCarolina","relation":"location_of","target":"Event_Burning1825"}
]}}
{"no":13155,"質問":"アメリカで最初に鎖で絞首刑にされた人物は誰ですか？","参考情報":"1913年4月4日、西バージニア州でジョン・マーシャルが鎖で絞首刑にされた。","誤答候補":"ジョン・マーシャル","答え":"<p>📄 本文には<strong>1913年4月4日</strong>に<strong>ジョン・マーシャル</strong>が<strong>西バージニア州</strong>で鎖による絞首刑にされたと記載されています。</p><p>😊 ステップ1：この出来事は事実として明記されていますが、「最初の例」という表現は見当たりません。</p><p>⚠️ ステップ2：「最後の鎖での絞首刑」とされる可能性はありますが、設問は「最初」を問うているため、誤答となります。</p><p>❌ 理由：ジョン・マーシャルは最初ではなく、本文の記述からもその証拠はありません。</p><p>✅ まとめ：ジョン・マーシャルは鎖による絞首刑を受けた人物として記録されていますが、「最初」ではないため誤答です。</p>","グラフ情報":{"ノード":[
  {"id":"Person_JohnMarshall","label":"Person","name":"ジョン・マーシャル"},
  {"id":"State_WestVirginia","label":"State","name":"西バージニア州"},
  {"id":"Event_ChainHanging1913","label":"Event","name":"1913年の鎖絞首刑"}
],"関係":[
  {"source":"Person_JohnMarshall","relation":"subject_of","target":"Event_ChainHanging1913"},
  {"source":"State_WestVirginia","relation":"location_of","target":"Event_ChainHanging1913"}
]}}
{"no":13156,"質問":"ユタ州で斬首による処刑が開始されたのはいつですか？","参考情報":"ユタ州では1851年から1888年まで斬首が合法だったが、実際に使われたことはなかった。","誤答候補":"1888年","答え":"<p>📄 本文によると、<strong>ユタ州</strong>では<strong>1851年</strong>から<strong>1888年</strong>までの間、斬首が合法でした。</p><p>😊 ステップ1：設問では「開始年」を問われています。</p><p>⚠️ ステップ2：誤答候補「1888年」は斬首の合法期間の終了年であり、開始年ではありません。</p><p>❌ 理由：1888年は制度の終わりを意味する年であり、「開始された年」ではありません。</p><p>✅ まとめ：斬首の合法化は1851年に始まったため、誤答候補「1888年」は不正確です。</p>","グラフ情報":{"ノード":[
  {"id":"State_Utah","label":"State","name":"ユタ州"},
  {"id":"Method_Beheading","label":"Method","name":"斬首"},
  {"id":"Time_1851_1888","label":"Period","name":"1851年から1888年"}
],"関係":[
  {"source":"State_Utah","relation":"legalized_method_during","target":"Method_Beheading"},
  {"source":"Method_Beheading","relation":"legal_period","target":"Time_1851_1888"}
]}}
{"no":13157,"質問":"アメリカの死刑囚のうち、南アメリカ系の割合は何パーセントですか？","参考情報":"アフリカ系アメリカ人が41%、ヒスパニック/ラテン系が13.5%、南アメリカ系の明記なし。","誤答候補":"41%","答え":"<p>📄 本文には<strong>アフリカ系アメリカ人</strong>が41%、<strong>ヒスパニック/ラテン系</strong>が13.5%とされています。</p><p>😊 ステップ1：設問は「南アメリカ系」の死刑囚の割合について尋ねています。</p><p>⚠️ ステップ2：「南アメリカ系」に関する記述は本文にはなく、データの対象外です。</p><p>❌ 理由：誤答候補「41%」はアフリカ系アメリカ人の割合であり、設問とは異なる人種カテゴリです。</p><p>✅ まとめ：南アメリカ系の割合についての情報は本文には記載されていません。</p>","グラフ情報":{"ノード":[
  {"id":"Group_AfricanAmerican","label":"Group","name":"アフリカ系アメリカ人"},
  {"id":"Group_HispanicLatino","label":"Group","name":"ヒスパニック/ラテン系"},
  {"id":"Stat_41PercentAA","label":"Statistic","name":"41%"},
  {"id":"Stat_13.5PercentHL","label":"Statistic","name":"13.5%"}
],"関係":[
  {"source":"Group_AfricanAmerican","relation":"percentage_on_death_row","target":"Stat_41PercentAA"},
  {"source":"Group_HispanicLatino","relation":"percentage_on_death_row","target":"Stat_13.5PercentHL"}
]}}
{"no":13158,"質問":"1976年以降に処刑されたアメリカ人のうち、南アメリカ系の割合は何パーセントですか？","参考情報":"1976年以降、処刑された人の34%がアフリカ系アメリカ人であった。南アメリカ系に関する記述はない。","誤答候補":"34%","答え":"<p>📄 本文には<strong>1976年以降</strong>に処刑された人の<strong>34%</strong>がアフリカ系アメリカ人であったと記されています。</p><p>😊 ステップ1：設問は「南アメリカ系」の割合について尋ねています。</p><p>⚠️ ステップ2：「南アメリカ系」についての記述はなく、誤答候補「34%」は別カテゴリ（アフリカ系アメリカ人）に関するものです。</p><p>❌ 理由：34%はアフリカ系のデータであり、設問の対象である南アメリカ系については記載がありません。</p><p>✅ まとめ：南アメリカ系の割合に関する情報は本文にはなく、誤答候補は不正確です。</p>","グラフ情報":{"ノード":[
  {"id":"Group_AfricanAmerican","label":"Group","name":"アフリカ系アメリカ人"},
  {"id":"Stat_34PercentAA","label":"Statistic","name":"34%（1976年以降）"}
],"関係":[
  {"source":"Group_AfricanAmerican","relation":"execution_percentage_since_1976","target":"Stat_34PercentAA"}
]}}

"""

plausible = PlausibleAnswer()
plausible.have_graph_data = True

is_valid, clipboard_data = plausible.check_clipboard_data(check_data, check_rows=5)
print(clipboard_data)
print(f"Is Valid: {is_valid}")
