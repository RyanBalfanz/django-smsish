"""
Dummy SMS backend that does nothing.
"""
from django.core.mail.backends.dummy import EmailBackend


class SMSBackend(EmailBackend):
	pass
