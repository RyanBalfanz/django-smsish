"""
SMS backend that writes messages to console instead of sending them.
"""
from django.core.mail.backends.console import EmailBackend


class SMSBackend(EmailBackend):
	pass
