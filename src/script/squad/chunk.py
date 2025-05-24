import json
import math
import os
from pathlib import Path


def chunk_dataset(
    input_path: str, output_dir: str, prefix: str, chunk_size: int = 1000
):
    # Create output directory (delete if exists)
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, file))
        print(f"🧹 Cleaned output dir: {output_dir}")
    else:
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Load full dataset
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    num_chunks = math.ceil(total / chunk_size)

    for i in range(num_chunks):
        chunk = data[i * chunk_size : (i + 1) * chunk_size]
        chunk_filename = f"{prefix}_{str(i+1).zfill(3)}.json"
        chunk_path = os.path.join(output_dir, chunk_filename)

        with open(chunk_path, "w", encoding="utf-8") as f:
            json.dump(chunk, f, ensure_ascii=False, indent=2)

        print(f"✅ Wrote {len(chunk)} records to {chunk_path}")

    print(f"🎉 Split {total} samples into {num_chunks} chunks in {output_dir}")


# Example usage
chunk_dataset(
    input_path="data/squad/processed/answers_dataset.json",
    output_dir="data/squad/processed/answers_chunks",
    prefix="answers",
    chunk_size=10,
)

chunk_dataset(
    input_path="data/squad/processed/plausible_answers_dataset.json",
    output_dir="data/squad/processed/plausible_chunks",
    prefix="plausible",
    chunk_size=10,
)
