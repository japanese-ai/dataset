from script.chat_gpt_ui import ChatGptUI
from script.util import (
    has_duplicate_emojis,
    has_html_tags,
    has_japanese,
    has_only_one_unique_emoji,
    is_valid_graph_info,
)


class PlausibleAnswer(ChatGptUI):
    def __init__(self):
        super().__init__()
        self.have_graph_data = False
        self.folder_path = "data/squad/processed/plausible_chunks"
        self.destination_file = "data/squad/plausible_translated.jsonl"
        self.get_data_y_cors = list(range(177, 588, 10))
        self.example_data = [
            '"グラフ情報":{"ノード":[{"id":"Visa_Student","label":"VisaType","name":"学生ビザ"},{"id":"Doc_CoE","label":"Document","name":"証明書"}],"関係":[{"source":"Visa_Student","relation":"requires_document","target":"Doc_CoE"}]}'
        ]

        self.new_chat_target_y_cor = 360

    def get_message(self, content, filename, index, num_rows):
        if self.have_graph_data:
            return f'"""\n{content}\n"""\nこのデータセット({filename}_{index})を、指定されたプロンプトに従って変換してください。具体的には、質問と参考情報と誤答候補を日本語に翻訳し、グラフ情報を必ず参照して、HTMLと絵文字を含むCoT形式の回答を生成してください。グラフ情報は必ず含め、誤答候補も出力してください。出力はJSONL形式でお願いします。出力は各データが1行として全て{num_rows}件とも表示されるようにしてください。\n※誤答候補は配列で出力しちゃダメ\n※答えにCoT形式をもっと詳しく入れて欲しい\n※答えにもっと絵文字を入れて欲しい\nグラフ情報は例の情報にならないように\n※ノードの「name」を日本語に翻訳して欲しい\n※関係のデータを忘れずに'

        return f'"""\n{content}\n"""\nこのデータセット({filename}_{index})を、指定されたプロンプトに従って変換してください。具体的には、質問と参考情報と誤答候補を日本語に翻訳し、HTMLと絵文字を含むCoT形式の回答を生成してください。誤答候補は必ず含めて出力してください。出力はJSONL形式でお願いします。出力は各データが1行として全て{num_rows}件とも表示されるようにしてください。\n※誤答候補は配列で出力しちゃダメ\n※答えにCoT形式をもっと詳しく入れて欲しい\n※答えにもっと絵文字を入れて欲しい'

    def is_valid_format(self, obj):
        required_keys = {"質問", "参考情報", "誤答候補", "答え"}

        if not isinstance(obj, dict):
            return False

        if not required_keys.issubset(obj.keys()):
            return False

        if not all(isinstance(obj[key], str) for key in required_keys):
            return False

        if (
            has_only_one_unique_emoji(obj.get("答え"))
            or has_duplicate_emojis(obj.get("答え"))
            or not has_html_tags(obj.get("答え"))
        ):
            return False

        for key in required_keys:
            if not has_japanese(obj.get(key)):
                return False

        if self.have_graph_data:
            if "グラフ情報" not in obj:
                return False
            if not is_valid_graph_info(obj["グラフ情報"], obj, ["答え"]):
                return False

        return True
