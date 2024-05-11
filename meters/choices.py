#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"
"""

MAP_STAGE_CHOICE = (
	("awaiting_kyc", "Awaiting KYC"),
	("awaiting_payment", "Awaiting Payment"),
	("awaiting_installation", "Awaiting Installation"),
	("awaiting_account_generation", "Awaiting Account Generation"),
	("awaiting_capture", "Awaiting Capture"),
	("completed", "Completed"),
)

PHASE_CHOICE = (
	("single_phase", "Single Phase"),
	("two_phase", "Two Phase"),
	("three_phase", "Three Phase"),
	("md", "MD"),
)

METER_APPLICATION_REQUEST_TYPE_CHOICE = (
	("new", "New"),
	("existing", "Existing"),
	("separation", "Separation"),
	("replacement", "Replacement"),
)

CUSTOMER_BAND_CHOICE = [
    ('Band A', (
        ('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ('A5', 'A5'),
    )
    ),
    ('Band B', (
        ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4'), ('B5', 'B5'),
    )
    ),
    ('Band C', (
        ('C1', 'C1'), ('C2', 'C2'), ('C3', 'C3'), ('C4', 'C4'), ('C5', 'C5'),
    )
    ),
    ('Band D', (
        ('D1', 'D1'), ('D2', 'D2'), ('D3', 'D3'), ('D4', 'D4'), ('D5', 'D5'),
    )
    ),
    ('Band E', (
        ('E1', 'E1'), ('E2', 'E2'), ('E3', 'E3'), ('E4', 'E4'), ('E5', 'E5'),
    )
    ),
]


PREMISES_TYPE_CHOICE = (
    ("residential", "Residential"),
    ("commercial", "Commercial"),
    ("industrial", "Industrial"),
    ("special", "Special"),
    ("others", "Others"),
)

def boot():
    pass

if __name__ == "__main__":
    boot()
