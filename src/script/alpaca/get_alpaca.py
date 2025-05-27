from script.alpaca.alpaca import Alpaca

alpaca = Alpaca()
alpaca.wait_time = 180
alpaca.start_get_data(start=90, start_from_new_chat=False)
