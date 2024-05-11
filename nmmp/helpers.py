#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"
"""
from nmmp.models import NMMPMeter
import re

def generateNMMPMeter(row, vendor, meter_phase):
    egg = {
        "vendor": vendor,
        "meter_number": row.get("meter_number"),
        "meter_phase": meter_phase,
        "carton_number": row.get("carton_number"),
        "SGC": row.get("SGC"),
        "FPU": row.get("FPU"),
    }
    return NMMPMeter(**egg)

def generatorNMMPMeter(rows, vendor, meter_phase):
    for row in rows:
        egg = {
            "vendor":vendor,
            "meter_number": row.get("meter_number"),
            "meter_phase": meter_phase,
            "carton_number": row.get("carton_number"),
            "SGC": row.get("SGC"),
            "FPU": row.get("FPU"),
        }
        yield NMMPMeter(**egg)


def getValidFPU(value):
    # dd.A.str.extract('(\d+\.\d+|\d+)')
    val = re.findall("\d+\.\d+|\d+", str(value) )
    if val:
        return " ".join(val)
    return None
    # return val

# dd['number'] = dd['A'].apply(lambda x: getValidFPU(x))

def boot():
    pass

if __name__ == "__main__":
    boot()
