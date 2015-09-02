import os
from distutils.core import setup
README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
setup(name='pyoneall',
    version='0.1.1',
    packages=['pyoneall'],
    license='MIT License, see LICENSE file',
    description='OneAll API wrapper (http://www.oneall.com). Provides unified API for 30+ social networks',
    long_description=README,
    url='http://www.leandigo.com/',
    author='Michael Greenberg / Leandigo',
    author_email='michael@leandigo.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',  # Could be more! Not tested yet.
        'Topic :: Security',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
)