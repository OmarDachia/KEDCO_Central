#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"
"""
RELIGION_CHOICE = (
    ("islam", "Islam"),
    ("christianity", "Christianity"),
    ("others", "Others"),
)

GENDER_CHOICE = (("male", "Male"), ("female", "Female"))

GUARDIAN_RELATION_WITH_STUDENT_CHOICE = (
    ("parent", "Parent"),
    ("father", "Father"),
    ("mother", "Mother"),
    ("sibling", "Sibling"),
    ("spouse", "Spouse"),
    ("others", "Others"),
)

ENTERY_LEVEL = (("fresh", "Fresh"), ("transfer", "Transfer"))

HEALTH_STATUS = (
    ("Good", "Good"),
    ("Sick", "Sick"),
    ("On Medication", "On Medication"),
    ("Others", "Others"),
)

ETHNICITY_CHOICE = (
    ("fulani", "Fulani"),
    ("hausa", "Hausa"),
    ("hausa-fulani", "Hausa-Fulani"),
    ("igbo", "Igbo"),
    ("yoruba", "Yoruba"),
    # ("tiv", "TIV"),
    # ("ibibio", "Ibibio"),
    # ("nupe", "Nupe"),
)

USER_TYPE_CHOICE = (("staff", "Staff"), ("admin", "Admin"), ("super_admin", "Super Admin"))


CLASS_TYPE = (
    ("education", "Education"),
    ("islamiyya", "Islamiyya"),
    ("Others", "Others"),
)

CLASS_CATEGORY = (
    ("pre_nursery", "Pre Nursery"),
    ("nursery", "Nursery"),
    ("play_group", "Play Group"),
    ("primary", "Primary"),
    ("sss", "Senior Secondary"),
    ("jsss", "Junior Secondary"),
    ("islamiyya", "Islamiyya"),
    ("others", "Others"),
)


TERMS = (
    ("1st Term", "1st Term"),
    ("2nd Term", "2nd Term"),
    ("3rd Term", "3rd Term"),
    ("Others", "Others"),
)

POST_STATUS_CHOICE = (
    ("draft", "Draft"),
    ("publish", "Publish"),
)

STATUS_CHOICE = (
    ("inactive", "Inactive"),
    ("active", "Active"),
)



def boot():
    pass


if __name__ == "__main__":
    boot()
