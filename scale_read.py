import serial
import serial.tools.list_ports
import glob
import yaml
import shutil

with open('/home/jordan/Desktop/nih_mice_beh/config.yaml','r') as file:
    cfg = yaml.load(file, Loader=yaml.FullLoader)

for file in glob.glob(cfg['main_path'] + "/*.csv"):
    shutil.move(file, cfg['transfer_path'])