from django.conf import settings
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage

from smsish.mail.utils import emailify_phone_number
from smsish.sms.backends.base import BaseSMSBackend

DEFAULT_SMS_OVER_EMAIL_BACKEND = "smsish.mail.backends.mailtrap.EmailBackend"


class SMSBackend(BaseSMSBackend):
	def __init__(self, *args, **kwargs):
		super(SMSBackend, self).__init__(*args, **kwargs)

	def send_messages(self, sms_messages):
		results = []
		for message in sms_messages:
			t = self.get_transform_function()
			email_message = t(message)
			result = email_message.send()
			results.append(result)

		return results

	def get_transform_function(self):
		return transform_sms_to_email_message


def transform_sms_to_email_message(sms_message):
	backend = getattr(settings, "SMSISH_MAILTRAP_SMS_BACKEND_EMAIL_BACKEND", DEFAULT_SMS_OVER_EMAIL_BACKEND)
	conn = get_connection(backend=backend)
	email = EmailMessage(
		subject="SMS over Email",
		body=sms_message.body,
		from_email=emailify_phone_number(sms_message.from_email),
		to=[emailify_phone_number(r) for r in sms_message.to],
		bcc=[emailify_phone_number(r) for r in sms_message.bcc] if sms_message.bcc else None,
		connection=conn,
		attachments=None,
		headers=None,
		cc=[emailify_phone_number(r) for r in sms_message.cc] if sms_message.cc else None,
		reply_to=[emailify_phone_number(sms_message.reply_to) for r in sms_message.reply_to] if sms_message.reply_to else None,
	)
	email.attach("metadata.txt", "Content-Length: {}".format(len(sms_message.body)), "text/plain")

	return email
