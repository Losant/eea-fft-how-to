# example from https://github.com/adafruit/Adafruit_CircuitPython_ADXL34x
import time
import board
import adafruit_adxl34x

i2c = board.I2C()  # uses board.SCL and board.SDA
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.data_rate = 3200

while True:
    print("%f %f %f"%accelerometer.acceleration)
    time.sleep(1)