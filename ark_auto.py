import time
from ppadb.client import Client
from ppadb.command import host
from PIL import Image
import numpy
import argparse
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

def run(device, args):
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

        device.shell("input touchscreen tap 2100 975")
        time.sleep(2)
        device.shell("input touchscreen tap 1880 785")
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
            if args.w <= checkPoint[0] == checkPoint[1] == checkPoint[2] <= 255:
                t2 = time.time()
                print(f"FINISHED\nStage time: {t2-t1} \n---------------------")
                finished = True
        time.sleep(DELAY_AFTER_FINISHED)
        device.shell(f"input touchscreen tap {args.x} {args.y} ")
        time.sleep(DELAY_BETWEEN_RUNS)
    print("COMPLETED")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=1,  help='Number of runs')
    parser.add_argument('-s', type=int, default=0,  help='Current Sanity')
    parser.add_argument('-c', type=int, default=0,  help='Cost of stage')
    parser.add_argument('-x', type=int, default='1500', help='detect point x')
    parser.add_argument('-y', type=int, default='620', help='detect point y')
    parser.add_argument('-w', type=int, default='180', help='white value')
    
    args = parser.parse_args()
    
    device = init()
    sys.stdout.write(str(run(device, args)))
    
if __name__ == "__main__":
    main()



