input_file = "data/squad/plausible_translated.jsonl"
output_file = "data/squad/plausible_translated_1.jsonl"

with open(input_file, "r", encoding="utf-8") as infile:
    lines = infile.readlines()

fixed_lines = []
for line in lines:
    # Strip newline for checking and add it back later
    stripped = line.rstrip("\n")
    if stripped.endswith("}]}"):
        # Replace only the exact ending
        stripped = stripped[:-3] + "}]}}"
    fixed_lines.append(stripped + "\n")

with open(output_file, "w", encoding="utf-8") as outfile:
    outfile.writelines(fixed_lines)
