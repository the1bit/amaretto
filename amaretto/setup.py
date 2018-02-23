"""Setuptools for amarett.
	AMArETTo - Azure MAnagEmenT by The1bit
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

import sys

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
	long_description = f.read()

# Get the license description from the license file
with open(path.join(here, 'LICENSE.txt'), encoding='utf-8') as l:
	license_description = l.read()


## Versin of the current package
currentVersion = "0.0.2.5"
sys.stdout.write("ammaretto: " + currentVersion + '\n')


# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(name='amaretto',
	version=currentVersion,
	description='Azure management tools by the1bit.',
	long_description=long_description + "\n" + license_description,
	url='https://github.com/the1bit/amaretto/tree/master/amaretto',
	author='Tibor Kiss',
	author_email='the1bithu@gmail.com',
	keywords='azure management python microsoft the1bithu',
	classifiers=[  # Optional
		# How mature is this project? Common values are
		#   3 - Alpha
		#   4 - Beta
		#   5 - Production/Stable
		'Development Status :: 3 - Alpha',

		# Indicate who your project is intended for
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'Operating System :: POSIX :: Linux',

		# Pick your license as you wish
		'License :: OSI Approved :: MIT License',

		# Specify the Python versions you support here. In particular, ensure
		# that you indicate whether you support Python 2, Python 3 or both.
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6'
	],
	  packages=['amaretto'],
	  license='MIT',
	  zip_safe=True)