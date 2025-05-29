from script.chat_gpt_ui import ChatGptUI
from script.util import (
    has_japanese,
    is_valid_answer,
    is_valid_graph_info,
    remove_html_tags,
)


class Alpaca(ChatGptUI):
    def __init__(self):
        super().__init__()
        self.input_file = "data/alpaca/processed/alpaca_data.jsonl"
        self.destination_file = "data/alpaca/alpaca.jsonl"
        self.get_data_y_cors = list(range(177, 588, 10))
        self.example_data = [
            '"グラフ情報":{"ノード":[{"id":"Visa_Student","label":"VisaType","name":"学生ビザ"},{"id":"Doc_CoE","label":"Document","name":"証明書"}],"関係":[{"source":"Visa_Student","relation":"requires_document","target":"Doc_CoE"}]}'
        ]

        self.new_chat_target_y_cor = 390

    def get_message(self, content, batch_str, num_rows):
        return f'"""\n{content}\n"""\nこのデータセット({batch_str}){num_rows}を、指定されたプロンプトに従って変換してください。具体的には、質問と参考情報と誤答候補を日本語に翻訳し、HTMLと絵文字を含むCoT形式の回答を生成してください。誤答候補は必ず含めて出力してください。出力はJSONL形式でお願いします。出力は各データが1行として全て{num_rows}件とも表示されるようにしてください。\n※「no」項目を忘れずに出力してください。\n※参考情報は必ず日本語に翻訳してください\n※参考情報は日本語に翻訳するだけでよい\n※答えにCoT形式が必要の場合をもっと詳しく入れて欲しい\n※答えにもっと絵文字を入れて欲しい\n※グラフ情報は例の情報にならないように\n※ノードの「name」を日本語に翻訳して欲しい\n※関係のデータを忘れずに'

    def is_valid_format(self, content, obj):
        required_keys = {"質問", "参考情報", "誤答候補", "答え"}
        japanese_keys = {"質問", "参考情報", "答え"}

        if not isinstance(obj, dict):
            return (
                False,
                f"Invalid type: Expected a dictionary, got {type(obj).__name__}",
            )

        if "no" not in obj:
            return False, "Missing required key: 'no'"

        if not isinstance(obj["no"], int):
            return False, "no must be a integer"

        if "cot" not in obj:
            return False, "Missing required key: 'cot'"

        if not isinstance(obj["cot"], bool):
            return False, "cot must be a boolean"

        if not required_keys.issubset(obj.keys()):
            return False, f"Missing required keys: {required_keys - obj.keys()}"

        if not all(isinstance(obj[key], str) for key in required_keys):
            return False, "All required keys must have string values"

        valid, message = is_valid_answer(obj.get("答え"), is_cot=obj.get("cot"))
        if not valid:
            return False, message

        remove_html_tags(obj["誤答候補"])

        for key in japanese_keys:
            if key == "参考情報" and obj.get(key).strip() == "":
                continue

            if not has_japanese(obj.get(key)):
                return False, f"{key} does not contain Japanese characters"

        if "グラフ情報" not in obj:
            return False, "Missing 'グラフ情報' key in the object"

        valid, message = is_valid_graph_info(obj["グラフ情報"], allow_empty_data=True)
        if not valid:
            return False, f"Invalid graph information: {message}"

        return True, ""
        valid, message = is_valid_graph_info(obj["グラフ情報"], allow_empty_data=True)
        if not valid:
            return False, f"Invalid graph information: {message}"

        return True, ""
