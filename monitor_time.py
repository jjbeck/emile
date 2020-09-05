from datetime import datetime
import time
import save_data

class monitor_time():

    def __init__(self):
        self.state = "feeding"


    def rasp_pi_monitor(self, config_params, hfd_or_chow, ser1=None, ser2=None):
        FED_prot = 0
        print(ser1)
        while True:
            time.sleep(3)
            if ser1:
                if hfd_or_chow == "CHOW":
                    ser1.write(config_params['CHOW protocol'][FED_prot].encode('utf-8'))
                    FED_prot += 1
                else:
                    ser1.write(config_params['HFD protocol'][FED_prot].encode('utf-8'))
                    FED_prot += 1
            if ser2:
                if hfd_or_chow == "CHOW":
                    ser2.write(config_params['CHOW protocol'][FED_prot].encode('utf-8'))
                    FED_prot += 1
                else:
                    ser2.write(config_params['HFD protocol'][FED_prot].encode('utf-8'))
                    FED_prot += 1





    def change_state(self):
        self.state == "no feeding"




