import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
	README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name='django-smsish',
	version='1.2.1',
	packages=[
		'smsish',
		'smsish.sms',
		'smsish.sms.backends',
	],
	include_package_data=True,
	license='MIT',  # example license
	description='A simple Django app to send SMS messages using an API similar to that of django.core.mail.',
	long_description=README,
	url='https://github.com/RyanBalfanz/django-smsish',
	author='Ryan Balfanz',
	author_email='ryan@ryanbalfanz.net',
	classifiers=[
		'Development Status :: 4 - Beta',
		# 'Development Status :: 5 - Production/Stable',
		'Environment :: Web Environment',
		'Framework :: Django',
		'Framework :: Django :: 1.8',
		'Framework :: Django :: 1.9',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Topic :: Communications',
		'Topic :: Communications :: Telephony',
	],
)
