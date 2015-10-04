# -*- coding: utf-8 -*-
from os.path import join, dirname

from setuptools import setup

README = open(join(dirname(__file__), 'README.rst')).read()
setup(
    name='pyoneall',
    version='0.2.3',
    packages=['pyoneall'],
    install_requires=['future'],
    license='MIT License, see LICENSE file',
    description='OneAll API wrapper (http://www.oneall.com). Provides unified API for 30+ social networks',
    long_description=README,
    test_suite='tests',
    url='http://www.leandigo.com/',
    author='Michael Greenberg / Leandigo',
    author_email='michael@leandigo.com',
    maintainer='Ekevoo',
    maintainer_email='ekevoo@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        # Python 3.2 is not supported because "future" is incompatible with it.
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
)
