from script.chat_gpt_ui import ChatGptUI
from script.util import (
    has_duplicate_emojis,
    has_html_tags,
    has_japanese,
    has_only_one_unique_emoji,
    is_valid_graph_info,
)


class Answer(ChatGptUI):
    def __init__(self):
        super().__init__()
        self.input_file = "data/squad/processed/answers_dataset.json"
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

    def get_message(self, content, batch_str, num_rows):
        no_str = "\n※「no」項目を忘れずに出力してください。" if self.have_no else ""
        if self.current_start_no > 43210:
            return f'"""\n{content}\n"""\nこのデータセット({batch_str}){num_rows}件を、指定されたプロンプトに従って変換してください。具体的には、質問と参考情報を必ず日本語に翻訳し、グラフ情報を必ず参照して、必ずHTMLと絵文字を含むCoT形式の回答を生成してください。グラフ情報は必ず含めて出力してください。出力はJSONL形式でお願いします。出力は各データが1行として全て{num_rows}件とも表示されるようにしてください。{no_str}\n※答えにCoT形式をもっと詳しく入れてほしい\n※答えにもっと絵文字を入れてほしい\nグラフ情報は例の情報にならないように\n※ノードの「name」を日本語に翻訳して欲しい\n※関係のデータを忘れずに'

        return f'"""\n{content}\n"""\nこのデータセット({batch_str}){num_rows}件を、指定されたプロンプトに従って変換してください。具体的には、質問と参考情報を必ず日本語に翻訳し、必ずHTMLと絵文字を含むCoT形式の回答を生成してください。出力はJSONL形式でお願いします。出力は各データが1行として全て{num_rows}件とも表示されるようにしてください。{no_str}\n※答えにCoT形式をもっと詳しく入れてほしい\n※答えにもっと絵文字を入れてほしい'

    def is_valid_format(self, obj):
        required_keys = {"質問", "参考情報", "答え"}

        if not isinstance(obj, dict):
            return (
                False,
                f"Invalid type: Expected a dictionary, got {type(obj).__name__}",
            )

        if self.have_no and "no" not in obj:
            return False, "Missing required key: 'no'"

        if not required_keys.issubset(obj.keys()):
            return False, f"Missing required keys: {required_keys - obj.keys()}"

        if not all(isinstance(obj[key], str) for key in required_keys):
            return False, "All required keys must have string values"

        if has_only_one_unique_emoji(obj.get("答え")):
            return False, "Only have one emoji in the answer"

        if has_duplicate_emojis(obj.get("答え")):
            return False, "Has duplicate emojis in the answer"

        if not has_html_tags(obj.get("答え")):
            return False, "Answer does not contain HTML tags"

        for key in required_keys:
            if not has_japanese(obj.get(key)):
                return False, f"{key} does not contain Japanese characters"

        if (self.have_no and obj.get("no") > 43210) or self.current_start_no > 43210:
            if "グラフ情報" not in obj:
                return False, "Missing 'グラフ情報' key in the object"

            valid, message = is_valid_graph_info(obj["グラフ情報"])
            if not valid:
                return False, f"Invalid graph information: {message}"

        return True, ""
