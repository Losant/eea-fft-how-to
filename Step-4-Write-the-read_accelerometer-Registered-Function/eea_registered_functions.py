#
# This module contains any registered functions. The functions and their
# imported names are returned as a dictionary at the bottom of this file.
# The code in eea_wasmer and eea_pywasm3 automatically imports from
# whatever is specified in this dictionary.
#
# You will have to modify this file for your use case.
#

import eea_utils

import board
import adafruit_adxl34x

def init(wasm_memory):


    def eea_fn_read_accelerometer(output0: float) -> int:
        print("reading accelerometer...")
        i2c = board.I2C()  # uses board.SCL and board.SDA
        accelerometer = adafruit_adxl34x.ADXL345(i2c)
        accelerometer.data_rate = 3200
        
        print("%f %f %f"%accelerometer.acceleration)
        
        # send only x-axis value
        x_axis_accel = accelerometer.acceleration[0]
        eea_utils.encode_float(wasm_memory, x_axis_accel, output0)

        return 0
        
    # Return a dictionary of import names and functions.
    # The "sig" values are required when using pywasm3. They are ignored for wasmer.
    return {
        "eea_fn_read_accelerometer":  {"sig": "i(i)",    "func": eea_fn_read_accelerometer}
    }
