"""SMS backend that writes messages to a file."""

from django.core.mail.backends.filebased import EmailBackend


class SMSBackend(EmailBackend):
	pass
