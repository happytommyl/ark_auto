import time
from ppadb.client import Client
from ppadb.command import host
from PIL import Image
import numpy
import argparse
import sys

def init():
    adb = Client(host='127.0.0.1', port=5037)
    devices = adb.devices()

    if len(devices) == 0:
        print('no devices found')
        quit()

    device = devices[0]
    return device

def run(device, args):
    for i in range(args.n):
        DELAY_BETWEEN_RUNS = 10
        DELAY_AFTER_FINISHED = 5
        
        print(i+1, ' : RUNNING')

        device.shell("input touchscreen tap 2100 975")
        time.sleep(3)
        device.shell("input touchscreen tap 1880 785")

        finished = False
        while not finished:
            time.sleep(5)
            image = device.screencap()

            with open('screen.png', 'wb') as f:
                f.write(image)

            image = Image.open('screen.png')
            image = numpy.array(image, dtype=numpy.uint8)

            checkPoint = image[825][661]
            if 209 <= checkPoint[0] == checkPoint[1] == checkPoint[2] <= 255:
                print("FINISHED\n---------------------")
                finished = True

        time.sleep(DELAY_AFTER_FINISHED)
        device.shell("input touchscreen tap 1500 620")
        time.sleep(DELAY_BETWEEN_RUNS)
    print("COMPLETED")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=1,  help='Number of runs')
    args = parser.parse_args()
    
    device = init()
    sys.stdout.write(run(device, args))
    
if __name__ == "__main__":
    main()



