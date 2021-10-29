#
# This module contains any registered functions. The functions and their
# imported names are returned as a dictionary at the bottom of this file.
# The code in eea_wasmer and eea_pywasm3 automatically imports from
# whatever is specified in this dictionary.
#
# You will have to modify this file for your use case.
#

import time

import eea_utils

import board
import adafruit_adxl34x


def init(wasm_memory):

    def eea_fn_read_accelerometer(output0: int, output0_length: int, output0_result_length: int, output1: int) -> int:
        print("reading accelerometer...")
        i2c = board.I2C()  # uses board.SCL and board.SDA
        accelerometer = adafruit_adxl34x.ADXL345(i2c)
        accelerometer.data_rate = 3200

        # List to append acceleration data to
        accel_data = []

        # number of accelerometer readings to make
        num_loops = 1024

        # Check to make sure the availabe output length is big enough for the encoding.
        if num_loops > output0_length:
            return

        # Read the accelerometer num_loops number of times.
        time_start = time.time()
        for i in range(num_loops):
            accel_data.append(accelerometer.acceleration[0])

        time_end = time.time()

        sample_rate = (time_end-time_start) / num_loops

        print("sample rate: %f" % sample_rate)

        eea_utils.encode_float(wasm_memory, sample_rate, output1)

        # Encode all the results
        for i in range(num_loops):
            eea_utils.encode_float(
                wasm_memory, accel_data[i], output0 + (i * 4))

        # Encode the number of items written
        eea_utils.encode_int(wasm_memory, num_loops, 4, output0_result_length)

        return 0

    #
    # Encodes a string to base64.
    #
    def eea_fn_base64_encode(ptr_str: int, str_len: int, out_ptr_encoded_str: int, str_buffer_len: int, out_ptr_encoded_str_len: int) -> int:
        print("eea_fn_base64_encode")
        input = eea_utils.decode_string(wasm_memory, ptr_str, str_len)
        encoded = base64.b64encode(input.encode("utf-8")).decode("utf-8")
        eea_utils.encode_string(
            wasm_memory, encoded, out_ptr_encoded_str, str_buffer_len, out_ptr_encoded_str_len)

        return 0

    # Return a dictionary of import names and functions.
    # The "sig" values are required when using pywasm3. They are ignored for wasmer.
    return {
        "eea_fn_read_accelerometer":  {"sig": "i(iiii)",    "func": eea_fn_read_accelerometer},
        "eea_fn_base64_encode":       { "sig": "i(iiii)",  "func": eea_fn_base64_encode }
    }
