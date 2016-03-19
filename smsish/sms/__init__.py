"""
Tools for sending SMS messages.
"""
from __future__ import unicode_literals

from django.conf import settings
from django.utils.module_loading import import_string

from smsish.sms.message import (
	SMSMessage,
)

__all__ = [
	'get_sms_connection',
	'send_sms',
	'send_mass_sms',
]


def get_sms_connection(backend=None, fail_silently=False, **kwds):
	"""Load an sms backend and return an instance of it.

	If backend is None (default) settings.SMS_BACKEND is used.

	Both fail_silently and other keyword arguments are used in the
	constructor of the backend.

	https://github.com/django/django/blob/master/django/core/mail/__init__.py#L28
	"""
	klass = import_string(backend or settings.SMS_BACKEND)
	return klass(fail_silently=fail_silently, **kwds)


def send_sms(message, from_number, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None):
	"""
	Easy wrapper for sending a single message to a recipient list. All members
	of the recipient list will see the other recipients in the 'To' field.

	If auth_user is None, the EMAIL_HOST_USER setting is used.
	If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

	Note: The API for this method is frozen. New code wanting to extend the
	functionality should use the EmailMessage class directly.

	https://github.com/django/django/blob/master/django/core/mail/__init__.py#L40
	"""
	connection = connection or get_sms_connection(username=auth_user, password=auth_password, fail_silently=fail_silently)
	mail = SMSMessage(message, from_number, recipient_list, connection=connection)

	return mail.send()


def send_mass_sms(datatuple, fail_silently=False, auth_user=None, auth_password=None, connection=None):
	"""
	Given a datatuple of (subject, message, from_email, recipient_list), sends
	each message to each recipient list. Returns the number of emails sent.

	If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
	If auth_user and auth_password are set, they're used to log in.
	If auth_user is None, the EMAIL_HOST_USER setting is used.
	If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

	Note: The API for this method is frozen. New code wanting to extend the
	functionality should use the EmailMessage class directly.

	https://github.com/django/django/blob/master/django/core/mail/__init__.py#L64
	"""
	import smsish.sms.backends.rq
	if isinstance(connection, smsish.sms.backends.rq.SMSBackend):
		raise NotImplementedError
	connection = connection or get_sms_connection(username=auth_user, password=auth_password, fail_silently=fail_silently)
	messages = [SMSMessage(message, from_number, recipient, connection=connection) for message, from_number, recipient in datatuple]
	return connection.send_messages(messages)
