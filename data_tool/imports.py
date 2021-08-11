import sys
import os
import time
import datetime
from pathlib import Path
from loguru import logger

def kwargs2str(**kwargs):
    str_list = [f"{k}: {v}" for k, v in kwargs.items()]
    return ", ".join(str_list)