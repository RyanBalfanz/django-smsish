# django-smsish

[![PyPI version](https://badge.fury.io/py/django-smsish.svg)](https://badge.fury.io/py/django-smsish)
[![Build Status](https://travis-ci.org/RyanBalfanz/django-smsish.svg)](https://travis-ci.org/RyanBalfanz/django-smsish)
[![Code Health](https://landscape.io/github/RyanBalfanz/django-smsish/master/landscape.svg?style=flat)](https://landscape.io/github/RyanBalfanz/django-smsish/master)
[![Coverage Status](https://coveralls.io/repos/github/RyanBalfanz/django-smsish/badge.svg?branch=develop)](https://coveralls.io/github/RyanBalfanz/django-smsish)

Installation
------------

Add `smsish` to your `INSTALLED_APPS` and set `SMS_BACKEND`.

	INSTALLED_APPS += (
		'smsish',
	)

	SMS_BACKEND_CONSOLE = 'smsish.sms.backends.console.SMSBackend'
	SMS_BACKEND_DUMMY = 'smsish.sms.backends.dummy.SMSBackend'
	SMS_BACKEND_TWILIO = 'smsish.sms.backends.twilio.SMSBackend'
	SMS_BACKEND = SMS_BACKEND_DUMMY

To use the Twilio backend set some additional settings as well.

	TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", None)
	TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", None)
	TWILIO_MAGIC_FROM_NUMBER = "+15005550006"  # This number passes all validation.
	TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", TWILIO_MAGIC_FROM_NUMBER)

Note: You must also `pip install twilio` to use the Twilio backend.
