##############################################################################
#
# Copyright (c) 2013 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Test App views.
"""
import os


FAVICON_PATH = os.path.join(os.path.dirname(__file__), 'favicon.ico')


class FavIcon:

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'image/x-icon')
        with open(FAVICON_PATH, 'rb') as img:
            return img.read()


class HelloWorld:
    name = 'Zope App'
