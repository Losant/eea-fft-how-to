#
# This module contains any registered functions. The functions and their
# imported names are returned as a dictionary at the bottom of this file.
# The code in eea_wasmer and eea_pywasm3 automatically imports from
# whatever is specified in this dictionary.
#
# You will have to modify this file for your use case.
#

def init(wasm_memory):

    # Return a dictionary of import names and functions.
    # The "sig" values are required when using pywasm3. They are ignored for wasmer.
    return {
        
    }
