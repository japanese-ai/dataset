from script.squad.plausible_answer import PlausibleAnswer

check_data = """
{"no":24310,"質問":"1884年、党ウィップは党の名前を何に変更したか？","参考情報":"1884年に党ウィップは名前を「アイルランド議会党」に変更し、新しい選挙プロセスを導入しました。","誤答候補":"アイルランド議会党","答え":"<p>📅 <strong>ステップ1:</strong> 質問は「1884年に変更された党の名称」です。</p><p>📝 <strong>ステップ2:</strong> 参考情報では、1884年に「アイルランド議会党」に名称が変更されたと明記されています。</p><p>🔁 <strong>ステップ3:</strong> この変更は、組織の明確化と政治的統一を目的としたものでした。</p><p>❌ <strong>誤答候補:</strong> 「アイルランド議会党」は本文に記載された正解です。</p><p>まとめ：1884年、党ウィップはその名称を「アイルランド議会党」に変更し、新体制を整えました。✅🇮🇪🏛️</p>","グラフ情報":{"ノード":[{"id":"Irish_Parliamentary_Party","label":"Political Party","name":"アイルランド議会党"},{"id":"1884","label":"Year","name":"1884年"}],"関係":[{"source":"Irish_Parliamentary_Party","relation":"renamed_in","target":"1884"}]}}
{"no":24311,"質問":"パーネルモデルは政府で何に置き換えられたか？","参考情報":"パーネルモデルは、アイルランド議会党の厳格な党規と構造に基づき、「臨時の非公式な集まり」を置き換えました。","誤答候補":"臨時の非公式な集まり","答え":"<p>🔄 <strong>ステップ1:</strong> 質問は「パーネルモデルが置き換えた対象」です。</p><p>📘 <strong>ステップ2:</strong> 参考情報では「臨時の非公式な集まり」がそれに該当するとあります。</p><p>🏗️ <strong>ステップ3:</strong> パーネルは制度的・規律的な党モデルを導入し、以前の非公式な方式を排除しました。</p><p>❌ <strong>誤答候補:</strong> 「臨時の非公式な集まり」は明記された正解です。</p><p>まとめ：パーネルモデルは、非公式な政治集団に代わる構造的な党組織として導入されました。✅⚙️🗳️</p>","グラフ情報":{"ノード":[{"id":"Parnellite_Model","label":"Political Model","name":"パーネルモデル"},{"id":"Ad_Hoc_Informal_Groupings","label":"Structure","name":"臨時の非公式な集まり"}],"関係":[{"source":"Parnellite_Model","relation":"replaced_with","target":"Ad_Hoc_Informal_Groupings"}]}}
{"no":24312,"質問":"英国の政党が候補者の選抜を確実にするために作ったものは？","参考情報":"英国の政党は、候補者が専門的に選ばれるように「新しい選抜手続きを導入」しました。","誤答候補":"新しい選抜手続き","答え":"<p>🧑‍⚖️ <strong>ステップ1:</strong> 質問は「候補者選抜を確実にする手段」です。</p><p>🗳️ <strong>ステップ2:</strong> 参考情報では「新しい選抜手続き」が導入されたと述べられています。</p><p>🔍 <strong>ステップ3:</strong> この手続きは政党が管理することで、選抜の公正性と一貫性が保証されました。</p><p>❌ <strong>誤答候補:</strong> 「新しい選抜手続き」は本文に記された正しい答えです。</p><p>まとめ：英国の政党は候補者選定の質を確保するため、新しい選抜手続きを導入しました。✅📄👥</p>","グラフ情報":{"ノード":[{"id":"New_Selection_Procedure","label":"Political Mechanism","name":"新しい選抜手続き"},{"id":"British_Parties","label":"Group","name":"英国の政党"}],"関係":[{"source":"New_Selection_Procedure","relation":"implemented_by","target":"British_Parties"}]}}
{"no":24313,"質問":"1884年、英国の政党で何が導入されたか？","参考情報":"1884年、パーネルは議会でMPが一括して投票することを義務付ける「党の誓約」を強制しました。","誤答候補":"党の誓約","答え":"<p>📝 <strong>ステップ1:</strong> 質問は「1884年に導入された制度」です。</p><p>🧾 <strong>ステップ2:</strong> 参考情報には「党の誓約」が明記されており、これはMPの投票行動の一体化を図るものでした。</p><p>🔒 <strong>ステップ3:</strong> この制度により、政党の統制力と効率が大きく向上しました。</p><p>❌ <strong>誤答候補:</strong> 「党の誓約」は正答として本文に示されています。</p><p>まとめ：1884年、パーネルにより「党の誓約」が導入され、政党の規律が強化されました。✅📋📊</p>","グラフ情報":{"ノード":[{"id":"Party_Pledge","label":"Political Commitment","name":"党の誓約"},{"id":"1884","label":"Year","name":"1884年"}],"関係":[{"source":"Party_Pledge","relation":"imposed_in","target":"1884"}]}}
{"no":24314,"質問":"党のファンドレイザーは通常、誰にリードされているか？","参考情報":"党のファンドレイザーは通常、「党のリーダー」によってリードされています。","誤答候補":"党のリーダー","答え":"<p>💰 <strong>ステップ1:</strong> 質問は「誰が党のファンドレイザーを指導するか」です。</p><p>👤 <strong>ステップ2:</strong> 参考情報では「党のリーダー」が主導するとされています。</p><p>🏛️ <strong>ステップ3:</strong> リーダーは資金調達において中心的役割を果たし、政治活動の継続に不可欠です。</p><p>❌ <strong>誤答候補:</strong> 「党のリーダー」は本文に記された正しい情報です。</p><p>まとめ：党のファンドレイザーは通常、党のリーダーによって主導されます。✅💼🎙️</p>","グラフ情報":{"ノード":[{"id":"Party_Leader","label":"Person","name":"党のリーダー"},{"id":"Fundraiser","label":"Activity","name":"ファンドレイザー"}],"関係":[{"source":"Party_Leader","relation":"leads","target":"Fundraiser"}]}}

"""

plausible = PlausibleAnswer()
plausible.have_graph_data = False

is_valid, clipboard_data, message = plausible.check_clipboard_data(
    check_data, check_rows=5
)
print(clipboard_data)
print(f"Is Valid: {is_valid}")
print(f"Message: {message}")
