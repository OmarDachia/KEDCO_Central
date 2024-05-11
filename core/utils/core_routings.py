#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"
"""
from django.contrib.auth.models import User
from accounts.models import UserProfile
import re
from django.core.exceptions import ValidationError


def getDeletedUser():
    user, created = User.objects.get_or_create(username='deleted_user')
    return user


def getSystemUser():
    user, created = User.objects.get_or_create(username='System')
    return user


def getDeletedUserProfile():
    try:
       profile = UserProfile.objects.get(user__username='deleted_user')
    except UserProfile.DoesNotExist as exp:
        user = getDeletedUser()
        profile = UserProfile(user=user, staff_id="deleted_user")
        profile.save()
    return profile

def validateAccountNumber(num):
    """ takes account number and validate if it's avalid account format Params:	num: string of account number"""
    try:
        if re.match("^[0-9]{2}/[0-9]{2}/[0-9]{2}/[0-9]{4}-[0-9]{2}$", num):
            return True
        else:
            return False
    except Exception:
        return False


def checkAccountNumber(account_number):
    try:
        if not validateAccountNumber(account_number):
            raise ValidationError(
                "Please enter a Valid KEDCO Account Number"
            )
    except Exception as exp:
        raise ValidationError(
            f"Please enter a Valid KEDCO Account Number. Error: {exp}")


def validatePhoneNumber(num, max_length=11):
    """ Utils Helper Function to Valid Nigerian Phone Number

    Args:
        num ([digis]): [phone number to validate]
        max_length (int, optional): [maximum length of phone number to use]. Defaults to 11.
    """
    pass
    
def is_valid_nimsa(nimsa_number):
    if re.match("CC/CEF/PR/[0-9]{4,5}", nimsa_number):
        return True
    else:
        return False

def boot():
    pass

if __name__ == "__main__":
    boot()
