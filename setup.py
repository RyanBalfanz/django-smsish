import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
	README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name='django-smsish',
	version='0.1',
	packages=['smsish'],
	include_package_data=True,
	license='MIT',  # example license
	description='A simple Django app to send SMS messages.',
	long_description=README,
	url='http://www.example.com/',
	author='Ryan Balfanz',
	author_email='ryan@ryanbalfanz.net',
	classifiers=[
		'Environment :: Web Environment',
		'Framework :: Django',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License', # example license
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		# Replace these appropriately if you are stuck on Python 2.
		'Programming Language :: Python :: 3',
		# 'Programming Language :: Python :: 3.2',
		# 'Programming Language :: Python :: 3.3',
		# 'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Topic :: Internet :: WWW/HTTP',
		# 'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	],
)
