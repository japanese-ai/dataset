from script.alpaca.alpaca import Alpaca

alpaca = Alpaca()
alpaca.new_chat_target_y_cor = 420
# alpaca.wait_time = 180
alpaca.start_get_data(start=1835, start_from_new_chat=False)
# alpaca.get_error_data(start_from_new_chat=False)
