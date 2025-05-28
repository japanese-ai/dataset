from script.squad.plausible_answer import PlausibleAnswer

plausible = PlausibleAnswer()
# plausible.start_get_data(start=0, start_from_new_chat=False)
# plausible.add_no_to_output()
plausible.have_no = True

# invalid_list = plausible.extract_invalid_data_from_output(
#     "temp/plausible_invalid_data.jsonl"
# )
# print(f"Invalid data count: {len(invalid_list)}")

plausible.fix_invalid_data(
    invalid_file="temp/plausible_invalid_data.jsonl",
    fix_file="temp/plausible_invalid_fixed_data.jsonl",
    start_from_new_chat=False,
)

# plausible.merge_fixed_data(
#     fixed_file="temp/plausible_invalid_fixed_data.jsonl",
# )
