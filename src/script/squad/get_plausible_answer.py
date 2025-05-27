from script.squad.plausible_answer import PlausibleAnswer

plausible = PlausibleAnswer()
# plausible.start_get_data(start=0, start_from_new_chat=False)
plausible.have_no = True
plausible.check_output_file_valid("data/squad/plausible_translated_error.jsonl")
