#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"
"""


qs = MeterApplication.objects.filter(meter_number__isnull=True)
for i in qs:
    print(i.account_number)
    try:
        #print(i.installation.meter_number)
        print(i.kyc.account_number)
    except Exception as exp:
        print(exp)


def boot():
    pass

if __name__ == "__main__":
    boot()
