"""Mailtrap (SMTP) email backend class."""
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend as SMTPBaseEmailBackend


class EmailBackend(SMTPBaseEmailBackend):
	"""
	A wrapper that manages the Mailtrap SMTP network connection.
	"""
	def __init__(self, host=None, port=None, username=None, password=None, fail_silently=False, **kwargs):
		super().__init__(
			host="mailtrap.io",
			port=465,
			username=settings.MAILTRAP_EMAIL_HOST_USER if username is None else username,
			password=settings.MAILTRAP_EMAIL_HOST_PASSWORD if password is None else password,
			use_tls=True,
			fail_silently=fail_silently,
		)
