import device_connect
import device_read
import argparse


def main():
    parser = argparse.ArgumentParser(description="Path to save file")
    parser.add_argument("-mp", "-main_path",
                        help="Directory where you want .csv file to be saved")

    args = parser.parse_args()
    return args.mp


if __name__ == "__main__":
    #mp = main()
    a = device_connect.device_connect()
    hc_devices, weigh_devices = a.check_devices()
    a.bind_address(hc_devices)
    config_param, highest_exp = device_read.read_config('/home/pi/Desktop/fed_device/emile/config.yaml')
    b = device_read.connect_devices(config_param['main_path'], weigh_devices, config_param, highest_exp)

#have while loop in here controlling "feeding" state. Once key is pressed send update to state
#and then save all data to local computer



