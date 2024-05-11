#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"
"""


CONNECTION_STATUS_CHOICES =  (
	("connected","Connected"),
	("not_connected","Not Connected"),
	)

STATUS_CHOICES =  (
		("owner","Owner"),
		("tenant","Tenant"),
	)

PHASE_CHOICES = (
		("1_phase","1 Phase"),
		("3_phase","3 Phase"),
	)

POLE_TYPE_CHOICES = (
		("concrete", "Concrete"),
		("wood", "Wood"),
		("steel", "Steel"),
		("temporary", "Temporary"),
		("---","---")
	)

SERVICE_WIRE_CONDITION = (
		("ok", "OK"),
		("undersized", "Undersized"),
		("jointed", "Jointed")
	)

UPRISER_CHOICES = (
		("1","Upriser 1"),
		("2","Upriser 2"),
		("3","Upriser 3"),
		("4","Upriser 4"),
		("5","Upriser 5"),
		("6","Upriser 6")
	)

FEEDER_CAPACITY = (
	("11kva","11KV"),
	("33kva","33KV")
)

FEEDER_TYPES = (
	("public", "Public"),
	("dedicated", "Dedicated")
)


FEEDER_LOCATIONS = (
	("urban","URBAN"),
	("rural","RURAL")
)


TRX_CAPACITY = (
	("", ""),
)

FEEDER_BAND_CHOICE = (
	("band_a", "Band A"),
	("band_b", "Band B"),
	("band_c", "Band C"),
	("band_d", "Band D"),
	("band_e", "Band E"),
)
def boot():
    pass

if __name__ == "__main__":
    boot()
