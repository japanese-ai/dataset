import json
import os
from pathlib import Path


def format_and_split(input_path: str, answers_path: str, plausible_path: str):
    # Delete existing output files if present
    for path in [answers_path, plausible_path]:
        if os.path.exists(path):
            os.remove(path)
            print(f"🗑️ Deleted: {path}")
        Path(path).parent.mkdir(parents=True, exist_ok=True)

    # Read raw SQuAD file
    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    answers_data = []
    plausible_data = []

    # Traverse and split
    for article in raw_data["data"]:
        for paragraph in article["paragraphs"]:
            context = paragraph["context"]

            for qa in paragraph["qas"]:
                question = qa["question"].strip()
                is_impossible = qa.get("is_impossible", False)

                if is_impossible:
                    plausible_answers = [
                        ans["text"] for ans in qa.get("plausible_answers", [])
                    ]
                    plausible_data.append(
                        {
                            "context": context,
                            "question": question,
                            "plausible_answers": plausible_answers,
                        }
                    )
                else:
                    answers = [ans["text"] for ans in qa.get("answers", [])]
                    answers_data.append(
                        {"context": context, "question": question, "answers": answers}
                    )

    # Save both datasets
    with open(answers_path, "w", encoding="utf-8") as f:
        json.dump(answers_data, f, ensure_ascii=False, indent=2)

    with open(plausible_path, "w", encoding="utf-8") as f:
        json.dump(plausible_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(answers_data)} answers to {answers_path}")
    print(f"✅ Saved {len(plausible_data)} plausible answers to {plausible_path}")


# Usage
format_and_split(
    input_path="data/squad/raw/train-v2.0.json",
    answers_path="data/squad/processed/answers_dataset.json",
    plausible_path="data/squad/processed/plausible_answers_dataset.json",
)
