import time
from ppadb.client import Client
from ppadb.command import host
from PIL import Image
import numpy
import argparse
from configparser import ConfigParser
import sys
import math


def init():
    adb = Client(host='127.0.0.1', port=5037)
    devices = adb.devices()

    if len(devices) == 0:
        print('no devices found')
        quit()

    device = devices[0]
    return device

def run(device, args, config):
    if(args.c * args.s != 0):
        n = math.floor(args.s / args.c)
    else:
        n = 1
    if args.n > 1:
        n = min(n, args.n)
    for i in range(n):
        DELAY_BETWEEN_RUNS = 4
        DELAY_AFTER_FINISHED = 3
        
        print(f'{i+1} / {n}: RUNNING')

        device.shell(f"input touchscreen tap {config['start_button_0']}")
        time.sleep(2)
        device.shell(f"input touchscreen tap {config['start_button_1']}")
        t1 = time.time()

        finished = False
        while not finished:
            time.sleep(5)
            image = device.screencap()

            with open('screen.png', 'wb') as f:
                f.write(image)

            image = Image.open('screen.png')
            image = numpy.array(image, dtype=numpy.uint8)

            checkPoint = image[825][661]
            if int(config['white_value']) <= checkPoint[0] == checkPoint[1] == checkPoint[2] <= 255:
                t2 = time.time()
                print(f"FINISHED\nStage time: {t2-t1} \n---------------------")
                finished = True
        time.sleep(DELAY_AFTER_FINISHED)
        device.shell(f"input touchscreen tap {config['detect_point']} ")
        time.sleep(DELAY_BETWEEN_RUNS)
    print("COMPLETED")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=1,  help='Number of runs')
    parser.add_argument('-s', type=int, default=0,  help='Current Sanity')
    parser.add_argument('-c', type=int, default=0,  help='Cost of stage')
    
    args = parser.parse_args()
    config = ConfigParser()
    config.read('config.ini')
    config = config['display']

    device = init()
    sys.stdout.write(str(run(device, args, config)))
    
if __name__ == "__main__":
    main()



