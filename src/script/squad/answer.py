from script.chat_gpt_ui import ChatGptUI
from script.util import is_valid_graph_info


class Answer(ChatGptUI):
    def __init__(self):
        super().__init__()
        self.have_graph_data = False
        self.folder_path = "data/squad/processed/answers_chunks"
        self.destination_file = "data/squad/translated.jsonl"
        self.get_data_y_cors = list(range(163, 473, 10))
        self.example_data = [
            '"グラフ情報":{"ノード":[{"id":"Visa_Student","label":"VisaType","name":"学生ビザ"},{"id":"Doc_CoE","label":"Document","name":"証明書"}],"関係":[{"source":"Visa_Student","relation":"requires_document","target":"Doc_CoE"}]}'
        ]

        self.new_chat_y_cor = 160
        self.new_chat_target_y_cor = 290
        self.message_x_cor = 635
        self.message_y_cor = 810
        self.message_put_x_cor = 1320
        self.message_put_y_cor = 850
        self.message_wait_x_cor = 1400
        self.message_wait_y_cor = 650
        self.copy_x_cor = 1230
        self.close_voice_x_cor = 900
        self.close_voice_y_cor = 850

    def get_message(self, content, filename, index, num_rows):
        if self.have_graph_data:
            return f'"""\n{content}\n"""\nこのデータセット({filename}_{index}){num_rows}件を、指定されたプロンプトに従って変換してください。具体的には、質問と参考情報を必ず日本語に翻訳し、グラフ情報を必ず参照して、必ずHTMLと絵文字を含むCoT形式の回答を生成してください。グラフ情報は必ず含めて出力してください。出力はJSONL形式でお願いします。出力は各データが1行として全て{num_rows}件とも表示されるようにしてください。\n※答えにCoT形式をもっと詳しく入れてほしい\n※答えにもっと絵文字を入れてほしい\nグラフ情報は例の情報にならないように\n※ノードの「name」を日本語に翻訳して欲しい\n※関係のデータを忘れずに'

        return f'"""\n{content}\n"""\nこのデータセット({filename}_{index}){num_rows}件を、指定されたプロンプトに従って変換してください。具体的には、質問と参考情報を必ず日本語に翻訳し、必ずHTMLと絵文字を含むCoT形式の回答を生成してください。出力はJSONL形式でお願いします。出力は各データが1行として全て{num_rows}件とも表示されるようにしてください。\n※答えにCoT形式をもっと詳しく入れてほしい\n※答えにもっと絵文字を入れてほしい'

    def is_valid_format(self, obj):
        required_keys = {"質問", "参考情報", "答え"}

        if not isinstance(obj, dict):
            return False

        if not required_keys.issubset(obj.keys()):
            return False
        if not all(isinstance(obj[key], str) for key in required_keys):
            return False

        if self.have_graph_data:
            if "グラフ情報" not in obj:
                return False
            if not is_valid_graph_info(obj["グラフ情報"]):
                return False

        if self.has_only_one_unique_emoji(obj.get("答え")) or self.has_duplicate_emojis(obj.get("答え")) or not self.has_html_tags(obj.get("答え")):
            return False

        return True
