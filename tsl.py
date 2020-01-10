import tsl2561
import time

if __name__ == "__main__":
    while(True):
        tsl = tsl2561.TSL2561(debug=True)
        print(tsl.lux())
        time.sleep(1)