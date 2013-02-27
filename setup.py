##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
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
"""zope.paste - wsgi applications in zope 3 using paste.deploy
"""
import os
from setuptools import setup, find_packages

def read_file(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="zope.paste",
    version='0.5.dev0',
    author="Sidnei da Silva and the Zope Community",
    author_email="zope-dev@zope.org",
    description="Zope 3 and PasteDeploy",
    long_description=\
        read_file('README.txt') + \
        '\n\n' + \
        read_file('multiple.txt') + \
        '\n\n' + \
        read_file('CHANGES.txt'),
    keywords="web wsgi application server paste",
    url="http://pypi.python.org/pypi/zope.paste",
    license='ZPL 2.1',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development'
        ],
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope',],
      include_package_data=True,
      zip_safe=False,
      extras_require={
        'test-app': [
            'zope.app.securitypolicy',
            'zope.app.zcmlfiles',
            'zope.security[untrustedpython]',
            ],
        'twisted': ['zope.app.twisted'],
        'zserver': ['zope.app.server'],
        },
      install_requires=[
            'setuptools',
            'PasteDeploy',
            'zope.interface',
            'zope.app.appsetup',
            'zope.app.wsgi'],
      entry_points = """
      [paste.app_factory]
      main = zope.paste.factory:zope_app_factory
      """)
