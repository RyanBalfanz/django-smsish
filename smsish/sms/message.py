from django.core.mail import EmailMessage


class SMSMessage(EmailMessage):
	"""
	https://docs.djangoproject.com/en/1.8/topics/email/#the-emailmessage-class
	"""
	def __init__(self, body, from_number, to, connection=None):
		bcc = None
		attachments = None
		headers = None
		cc = None
		reply_to = None
		super().__init__(None, body, from_number, to, bcc, connection, attachments, headers, cc, reply_to)

	def get_connection(self, fail_silently=False):
		from smsish.sms import get_sms_connection as get_connection
		if not self.connection:
			self.connection = get_connection(fail_silently=fail_silently)
		return self.connection
