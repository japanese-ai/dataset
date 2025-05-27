from script.squad.answer import Answer

check_data = """
{"質問":"誰が1849年にパレルモの支配権を取り戻しましたか？","参考情報":"シチリア王国のブルボン家は、1849年にパレルモを再征服しました。ブルボン家の支配は、ジュゼッペ・ガリバルディが登場するまで続きました。","答え":"<p><strong>ブルボン家</strong>は1849年に<strong>パレルモ</strong>を再征服しました🏰。<br>ブルボン家の支配はシチリア王国にとって重要な歴史的な出来事であり、特にパレルモの再征服はその象徴的な瞬間でした⚔️。<br>パレルモはこの後、ガリバルディの軍隊によって占領されることになりますが、それまではブルボン家の支配下にありました📜。<br><p>✅ 1849年にパレルモを再征服したのはブルボン家です。</p>","グラフ情報":{"ノード":[{"id":"Bourbon_Family","label":"Family","name":"ブルボン家"},{"id":"Palermo","label":"City","name":"パレルモ"}],"関係":[{"source":"Bourbon_Family","relation":"regained_control_of","target":"Palermo"}]}}

{"質問":"1861年にシチリアとパレルモはどの王国に組み込まれましたか？","参考情報":"1861年に、シチリアとパレルモはイタリア王国の一部となりました。","答え":"<p><strong>1861年</strong>に、シチリアと<strong>パレルモ</strong>は<strong>イタリア王国</strong>に組み込まれました🇮🇹。<br>これはイタリア統一の重要な一歩であり、シチリアとパレルモが新しい国の一部となる瞬間でした🌍。<br>シチリアとパレルモはその後、イタリア王国の発展に大きな役割を果たしました📈。<br><p>✅ 1861年、シチリアとパレルモはイタリア王国に組み込まれました。</p>","グラフ情報":{"ノード":[{"id":"Kingdom_of_Italy","label":"Kingdom","name":"イタリア王国"},{"id":"Sicily","label":"Region","name":"シチリア"},{"id":"Palermo","label":"City","name":"パレルモ"}],"関係":[{"source":"Sicily","relation":"became_part_of","target":"Kingdom_of_Italy"},{"source":"Palermo","relation":"became_part_of","target":"Kingdom_of_Italy"}]}}

{"質問":"1866年の一週間にわたる反乱で誰が責任を問われましたか？","参考情報":"1866年、パレルモで一週間にわたる人気の反乱が起こり、イタリア政府はアナーキストと教会（特にパレルモ大司教）を責任者としました。","答え":"<p><strong>アナーキスト</strong>と<strong>教会</strong>（特に<strong>パレルモ大司教</strong>）が1866年の反乱で責任を問われました🔍。<br>反乱後、イタリア政府はこれらのグループを非難し、シチリアや教会に対する反発的な政策を導入しました📜。<br>反乱の原因やその後の政治的な影響は、シチリアの歴史において重要な転換点となりました⚖️。<br><p>✅ 1866年の反乱で責任を問われたのはアナーキストと教会（特にパレルモ大司教）です。</p>","グラフ情報":{"ノード":[{"id":"Anarchists","label":"Group","name":"アナーキスト"},{"id":"Church","label":"Institution","name":"教会"},{"id":"Palermo_Archbishop","label":"Person","name":"パレルモ大司教"}],"関係":[{"source":"Anarchists","relation":"blamed_for","target":"Rebellion"},{"source":"Church","relation":"blamed_for","target":"Rebellion"},{"source":"Palermo_Archbishop","relation":"blamed_for","target":"Rebellion"}]}}

{"質問":"パレルモで文化的、産業的、経済的成長を促進した家族はどれですか？","参考情報":"パレルモの文化的、産業的、経済的成長は、フローリオ家、デュクロ家、ルテッリ家、サンドロン家、ウィテカー家、ウツヴェッジオ家などの家族によって促進されました。","答え":"<p><strong>フローリオ家</strong>、<strong>デュクロ家</strong>、<strong>ルテッリ家</strong>、<strong>サンドロン家</strong>、<strong>ウィテカー家</strong>、<strong>ウツヴェッジオ家</strong>などの家族がパレルモでの<strong>文化的</strong>、<strong>産業的</strong>、<strong>経済的</strong>成長を促進しました💡。<br>これらの家族はシチリアにおける発展の重要な推進力となり、新しい産業や文化の発展を支えました🏭。<br>彼らの支援により、パレルモは新しい時代に向けて成長しました📈。<br><p>✅ パレルモで成長を促進した家族にはフローリオ家、デュクロ家、ルテッリ家、サンドロン家、ウィテカー家、ウツヴェッジオ家が含まれます。</p>","グラフ情報":{"ノード":[{"id":"Florio_Family","label":"Family","name":"フローリオ家"},{"id":"Ducrot_Family","label":"Family","name":"デュクロ家"},{"id":"Rutelli_Family","label":"Family","name":"ルテッリ家"},{"id":"Sandron_Family","label":"Family","name":"サンドロン家"},{"id":"Whitaker_Family","label":"Family","name":"ウィテカー家"},{"id":"Utveggio_Family","label":"Family","name":"ウツヴェッジオ家"}],"関係":[{"source":"Florio_Family","relation":"promoted_growth_in","target":"Palermo"},{"source":"Ducrot_Family","relation":"promoted_growth_in","target":"Palermo"},{"source":"Rutelli_Family","relation":"promoted_growth_in","target":"Palermo"},{"source":"Sandron_Family","relation":"promoted_growth_in","target":"Palermo"},{"source":"Whitaker_Family","relation":"promoted_growth_in","target":"Palermo"},{"source":"Utveggio_Family","relation":"promoted_growth_in","target":"Palermo"}]}}

{"質問":"新しく拡大したパレルモのヴィラはどのスタイルで建てられましたか？","参考情報":"新しく拡大したパレルモのヴィラは、アール・ヌーヴォー様式で建てられました。多くのヴィラはエルネスト・バジーレによってデザインされ、グランドホテル・ヴィラ・イジェアなどがその例です。","答え":"<p>新しく拡大した<strong>パレルモ</strong>のヴィラは<strong>アール・ヌーヴォー</strong>様式で建てられました🏰。<br>エルネスト・バジーレによって設計されたヴィラは、パレルモの新しい文化的な顔を作り上げました🖼️。<br>特に<strong>グランドホテル・ヴィラ・イジェア</strong>は、アール・ヌーヴォー様式の代表例として有名です🌟。<br><p>✅ 新しく拡大したパレルモのヴィラはアール・ヌーヴォー様式で建てられました。</p>","グラフ情報":{"ノード":[{"id":"Art_Nouveau","label":"Style","name":"アール・ヌーヴォー"},{"id":"Palermo_Villas","label":"Building","name":"パレルモのヴィラ"}],"関係":[{"source":"Art_Nouveau","relation":"influenced","target":"Palermo_Villas"}]}}


"""

answer = Answer()
answer.have_graph_data = True

is_valid, clipboard_data, message = answer.check_clipboard_data(
    check_data, check_rows=5
)
print(clipboard_data)
print(f"Is Valid: {is_valid}")
print(f"Message: {message}")
