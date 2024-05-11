#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shu'aib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2020, salafi'
__version__ = "0.01t"
"""

from django.conf import settings
import traceback
import logging
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback
from rest_framework import exceptions, status
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse

logger = logging.getLogger("django_error")

def drf_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        if isinstance(exc, Http404):
            exc = exceptions.NotFound()
        elif isinstance(exc, PermissionDenied):
            exc = exceptions.PermissionDenied()

        if isinstance(exc, exceptions.APIException):
            headers = {}
            if getattr(exc, 'auth_header', None):
                headers['WWW-Authenticate'] = exc.auth_header
            if getattr(exc, 'wait', None):
                headers['Retry-After'] = '%d' % exc.wait

            if isinstance(exc.detail, (list, dict)):
                data = exc.detail
            else:
                data = {'detail': exc.detail}

            set_rollback()
            response = Response(data, status=exc.status_code, headers=headers)

        response.data["status_code"] = response.status_code
        # TODO: send mail
        message = f"{exc}"
        logger.info(f"[API ErrorHandlerMiddleware]: {message}")
        return response
