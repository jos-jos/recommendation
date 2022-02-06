import os
import sys
import json

def readJS(name):
    with open(os.path.join(sys.path[0], name), "r") as f:
        text_dir = json.load(f)
    return text_dir