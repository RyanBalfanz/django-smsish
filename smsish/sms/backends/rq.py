"""SMS backend that enqueues messages to be sent."""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import django_rq

from smsish.sms import get_sms_connection
from smsish.sms.backends.base import BaseSMSBackend


class SMSBackend(BaseSMSBackend):
	"""
	An SMSBackend which sends messages asynchronously with the help of RQ.
	"""
	def __init__(self, backend=None, fail_silently=None, **kwargs):
		super(SMSBackend, self).__init__(fail_silently=fail_silently, **kwargs)

		SMSISH_RQ_SMS_BACKEND = getattr(settings, "SMSISH_RQ_SMS_BACKEND", None)
		if backend is None and SMSISH_RQ_SMS_BACKEND is None:
			raise ImproperlyConfigured("SMSISH_RQ_SMS_BACKEND is required but missing")

		self.backend = SMSISH_RQ_SMS_BACKEND if backend is None else backend

	def send_messages(self, sms_messages):
		"""
		Receives a list of SMSMessage instances and returns a list of RQ `Job` instances.
		"""
		results = []
		for message in sms_messages:
			try:
				assert message.connection is None
			except AssertionError:
				if not self.fail_silently:
					raise
			backend = self.backend
			fail_silently = self.fail_silently
			result = django_rq.enqueue(self._send, message, backend=backend, fail_silently=fail_silently)
			results.append(result)
		return results

	def _send(self, sms_message, backend=None, fail_silently=False):
		send_sms_message(sms_message, backend=backend, fail_silently=fail_silently)


def send_sms_message(sms_message, backend=None, fail_silently=False):
	"""
	Send an SMSMessage instance using a connection given by the specified `backend`.
	"""
	with get_sms_connection(backend=backend, fail_silently=fail_silently) as connection:
		result = connection.send_messages([sms_message])
	return result
