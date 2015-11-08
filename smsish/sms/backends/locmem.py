"""
Backend for test environment.
"""

from django.core import mail
from django.core.mail.backends.locmem import EmailBackend


class SMSBackend(EmailBackend):
	"""A SMS backend for use during test sessions.
	The test connection stores SMS messages in a dummy outbox,
	rather than sending them out on the wire.
	The dummy outbox is accessible through the outbox instance attribute.
	"""
	def __init__(self, *args, **kwargs):
		super(SMSBackend, self).__init__(*args, **kwargs)
		if not hasattr(mail, 'outbox'):
			mail.outbox = []

	def send_messages(self, messages):
		"""Redirect messages to the dummy outbox"""
		msg_count = 0
		for message in messages:  # .message() triggers header validation
			message.message()
			msg_count += 1
		mail.outbox.extend(messages)
		return msg_count
