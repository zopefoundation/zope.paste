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

from setuptools import find_packages
from setuptools import setup


def read_file(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


TEST_APP_REQUIRES = [
    'waitress',
    'zope.app.publication',
    'zope.authentication',
    'zope.browserpage',
    'zope.component',
    'zope.error',
    'zope.principalregistry',
    'zope.publisher',
    'zope.security',
    'zope.site',
    'zope.traversing',
    'zope.testrunner',
]
setup(
    name="zope.paste",
    version='1.1.0',
    author="Sidnei da Silva and the Zope Community",
    author_email="zope-dev@zope.org",
    description="Zope 3 and PasteDeploy",
    long_description=read_file('README.rst') +
    '\n\n' +
    read_file('multiple.rst') +
    '\n\n' +
    read_file('CHANGES.rst'),
    keywords="web wsgi application server paste",
    url="https://github.com/zopefoundation/zope.paste",
    license='ZPL 2.1',
    classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Zope Public License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: Implementation :: CPython',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Software Development',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['zope', ],
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'test-app': TEST_APP_REQUIRES,
        'test': TEST_APP_REQUIRES,
    },
    install_requires=[
        'setuptools',
        'PasteDeploy',
        'zope.interface',
        'zope.app.appsetup',
        'zope.app.wsgi'],
    tests_require=TEST_APP_REQUIRES,
    test_suite='zope.paste.tests.test_suite',
    entry_points="""
      [paste.app_factory]
      main = zope.paste.factory:zope_app_factory
      [console_scripts]
      serve = zope.paste.serve:serve
      """)
