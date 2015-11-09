"""SMTP SMS backend class."""
from django.core.mail.backends.smtp import EmailBackend


class SMSBackend(EmailBackend):
	"""
	A wrapper that manages the SMTP network connection.
	"""
	def __init__(self, *args, **kwargs):
		super(SMSBackend, self).__init__(*args, **kwargs)
