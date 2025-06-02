from script.alpaca.alpaca import Alpaca

alpaca = Alpaca()
alpaca.max_in_chat = 20
# alpaca.max_error_count = 10
alpaca.new_chat_target_y_cor = 450
# alpaca.wait_time = 180
alpaca.start_get_data(start=7845, start_from_new_chat=False)
# alpaca.get_error_data(start_from_new_chat=False)
