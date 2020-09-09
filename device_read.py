import serial
import threading
import save_data
from pynput import keyboard
import device_connect
import sys
import yaml
import time
from datetime import datetime
from datetime import date
import live_plot
import subprocess
import shutil
import glob
import smtplib, ssl

def read_config(config_path):
    try:
        with open(config_path, 'r') as file:
            cfg = yaml.load(file, Loader=yaml.FullLoader)
            exp_num = []
            for key in cfg:
                if 'experiment' in key:
                    exp_num.append(str(key[-1]))

            return cfg, max(exp_num)
    except FileNotFoundError:
        print("Wrong config file or config file path. Using default protocol")
        pass

    return {'main_path': '/home/jordan/Desktop/nih_mice_beh/', 'experiment 1': {'HFD protocol': '0,1,2', 'CHOW protocol': '0,1,2', 'date': '{}'.format(date.today())}}, 1

def write_config(config_path):
    print("write")

class connect_devices():

    def __init__(self,file_save_path, weigh_devices, config_param, experiment_number):

        self.port = 465  # For SSL
        self.smtp_server = "smtp.gmail.com"
        self.sender_email = "krashlabfed@gmail.com"  # Enter your address
        self.receiver_email1 = "jordan_becker@brown.edu"  # Enter receiver address
        self.receiver_email2 = "amysutto@gmail.com"
        self.password = "krasheslab"
        self.message = """\
        Subject: FED jammed

        This message is sent from a Krashes FED device."""

        self.config_param = config_param
        self.experiment_number = experiment_number
        for key in config_param:
            if "experiment" in key:
                if self.experiment_number in key:
                    self.experiment = key
        self.file_path = file_save_path
        #further on, include argument to save files to specific location
        self.save_data = save_data.save_data(file_save_path)
        try:
            self.ser1 = serial.Serial('/dev/rfcomm0', 9600)
            self.thread1 = threading.Thread(target=self.read_ser1, args=(self.ser1,))
            self.thread1.start()
        except:
            print("can't connect FED 1")
            ser1=None
            pass
        try:
            self.ser2 = serial.Serial('/dev/rfcomm1', 9600)
            self.thread2 = threading.Thread(target=self.read_ser2, args=(self.ser2,))
            self.thread2.setDaemon(True)
            self.thread2.start()
        except:
            print("Can't connect FED 2")
            ser2=None
            pass
        try:
            self.ser_weigh1 = serial.Serial(weigh_devices[0], 57600)
            self.thread8 = threading.Thread(target=self.read_ser_weigh1, args=(self.ser_weigh1,))
            self.thread8.setDaemon(True)
            self.thread8.start()
        except:
            print("cant connect scale")
            pass

        live_plt = live_plot.live_plot()

    def read_ser1(self,ser):

        with keyboard.Listener(on_press=self.on_press) as listener:
            while True:
                line = ser.readline().decode()
                if '.CSV' in line:
                    filen_name = self.save_data.ser_filename(line)
                    i = 0
                    continue
                if '1.1.44' in line and i == 0:
                    self.ser1_file_name = self.save_data.get_filename_paradigm(line, filen_name, self.experiment_number)
                    if 'HFD' in self.ser1_file_name:
                        self.thread3 = threading.Thread(target=self.rasp_pi_monitor, args=(self.config_param[self.experiment], 'HFD', self.ser1, "ser1", ))
                        self.thread3.setDaemon(True)
                        self.thread3.start()
                    else:
                        self.thread3 = threading.Thread(target=self.rasp_pi_monitor, args=(self.config_param[self.experiment], 'CHOW', self.ser1, "ser1", ))
                        self.thread3.setDaemon(True)
                        self.thread3.start()
                    i += 1
                if "20 motor rotations" in line:
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                        server.login(self.sender_email, self.password)
                        server.sendmail(self.sender_email, self.receiver_email1, self.message)
                        server.sendmail(self.sender_email, self.receiver_email2, self.message)
                if 'MM:DD:YYYY' in line:
                    header = self.save_data.universal_header(line)
                    self.save_data.ser1_df(header)
                    continue
                self.save_data.append_data(ser1=line, ser1_file=self.ser1_file_name)
            listener.join()

    def read_ser2(self,ser):

        while True:
            line = ser.readline().decode()
            if '.CSV' in line:
                filen_name = self.save_data.ser_filename(line)
                self.i = 0
                continue
            if '1.1.44' in line and self.i == 0:
                self.ser2_file_name = self.save_data.get_filename_paradigm(line, filen_name, self.experiment_number)
                if 'HFD' in self.ser2_file_name:
                    self.thread4 = threading.Thread(target=self.rasp_pi_monitor, args=(self.config_param[self.experiment], 'HFD', self.ser2, "ser2", ))
                    self.thread4.setDaemon(True)
                    self.thread4.start()
                    print("HFD")
                else:
                    self.thread4 = threading.Thread(target=self.rasp_pi_monitor, args=(self.config_param[self.experiment], 'CHOW', self.ser2, "ser2", ))
                    self.thread4.setDaemon(True)
                    self.thread4.start()
                    print("CHOW")
                self.i += 1
            if "20 motor rotations" in line:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                    server.login(self.sender_email, self.password)
                    server.sendmail(self.sender_email, self.receiver_email1, self.message)
                    server.sendmail(self.sender_email, self.receiver_email2, self.message)
            if 'MM:DD:YYYY' in line:
                header = self.save_data.universal_header(line)
                self.save_data.ser2_df(header)
                continue
            self.save_data.append_data(ser2=line, ser2_file=self.ser2_file_name)

    def read_ser_weigh1(self, ser):
        self.save_data.ser_weigh1(['Weight'])
        while True:
            line = ser.readline().decode()
            if line[1].isdigit():
                self.save_data.append_data(ser_weigh=line)


    def on_press(self,key):
        if key == keyboard.Key.end:
            print("Stopping data transfer. Files can be viewed in {}".format(self.file_path))
            self.ser1.close()
            subprocess.run("echo 1nickhong123| sudo rfcomm release rfcomm0", shell=True)
            self.thread1.join()
            sys.exit()

    def rasp_pi_monitor(self, config_params, hfd_or_chow, ser, ser1_or_ser2):
        FED_prot = 0

        while True:
            tm = datetime.now()
            tm_min = tm.minute
            tm_hour = tm.hour
            if tm_hour == 11 and tm_min == 45:
                try:
                    if hfd_or_chow == "CHOW":
                        ser.write(config_params['CHOW protocol'][FED_prot].encode('utf-8'))
                        FED_prot += 1
                        time.sleep(80)
                    else:
                        ser.write(config_params['HFD protocol'][FED_prot].encode('utf-8'))
                        FED_prot += 1
                        time.sleep(80)
                except IndexError:
                    print("Done with all FED protocols. Exiting")
                    if ser1_or_ser2 == "ser1":
                        self.ser1.close()
                        for file in glob.glob(self.config_param['main_path'] + "*.csv"):
                            shutil.move(file, self.config_param['transfer_path'])
                        subprocess.run("echo 1nickhong123| sudo rfcomm release rfcomm1", shell=True)
                        self.thread1.join()
                        sys.exit()






