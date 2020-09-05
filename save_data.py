import csv
import pandas as pd
import os

def calc_weight_derivate():
    print("calculated")

class save_data():

    def __init__(self, file_save_path):
        self.file_save_path = file_save_path
    def get_filename_paradigm(self,line, file_name, experiment_number):
        str_split = line.split(',')
        self.paradigm = str_split[5]
        self.device_num = str_split[2]
        if 0 <= int(self.device_num) <= 7:
            self.filename = file_name.replace('.CSV','_{}_M_CHOW_{}.csv'.format(self.paradigm, experiment_number))
        if 8 <= int(self.device_num) <= 14:
            self.filename = file_name.replace('.CSV','_{}_M_HFD_{}.csv'.format(self.paradigm, experiment_number))
        if 15 <= int(self.device_num) <= 21:
            self.filename = file_name.replace('.CSV','_{}_F_CHOW_{}.csv'.format(self.paradigm, experiment_number))
        if 22 <= int(self.device_num) <= 28:
            self.filename = file_name.replace('.CSV','_{}_F_HFD_{}.csv'.format(self.paradigm, experiment_number))

        return self.filename
    def universal_header(self, header):
        self.header = header.replace('\r\n','')
        self.header = header.split(',')
        return self.header
    def ser_filename(self, filename):
        self.ser_file = filename.replace('\r\n','')
        return self.ser_file
    def ser1_df(self,header):
        self.ser1_df =  pd.DataFrame(columns=[header])
    def ser2_df(self,header):
        self.ser2_df =  pd.DataFrame(columns=[header])
    def ser_weigh1(self,header):
        self.ser_weigh1_df = pd.DataFrame(columns=['Weight'])


    def append_data(self,ser1=None, ser1_file=None, ser2=None, ser2_file=None,
                    ser_weigh=None, ser_weigh_filename=None):
        if ser1:
            ser1_line = ser1.split(",")
            df_loc = len(self.ser1_df)
            self.ser1_df.loc[df_loc] = ser1_line
            self.ser1_df.to_csv(self.file_save_path + ser1_file,mode='w')

        if ser2:
            ser2_line = ser2.split(",")
            df_loc = len(self.ser2_df)
            self.ser2_df.loc[df_loc] = ser2_line
            self.ser2_df.to_csv(self.file_save_path + ser2_file, mode='w')

        if ser_weigh:
            df_loc = len(self.ser_weigh1_df)
            self.ser_weigh1_df.loc[df_loc] = ser_weigh
            self.ser_weigh1_df.to_csv(self.file_save_path + "weight_test.csv", mode='w')



