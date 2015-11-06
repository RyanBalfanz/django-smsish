from django.test import TestCase
from django.test.utils import override_settings

from smsish.sms import send_sms
from smsish.sms.message import SMSMessage

FROM_NUMBER = "+15005550006"
TO_NUMBER = "+15005550006"


class SMSMessageTestCase(TestCase):
	def setUp(self):
		self.sms = SMSMessage(
			"Body",
			FROM_NUMBER,
			[TO_NUMBER]
		)
		self.sms_no_recipients = SMSMessage("Body", TO_NUMBER, [])

	def test_create_with_subject_not_allowed(self):
		with self.assertRaises(TypeError):
			SMSMessage("Subject", "Body", FROM_NUMBER, [TO_NUMBER])

	def test_recipients(self):
		sms = self.sms
		recipients = sms.recipients()
		self.assertEqual(recipients, [TO_NUMBER])

	def test_send(self):
		sms = self.sms
		numSent = sms.send()
		self.assertEqual(numSent, 1)

		sms_no_recipients = self.sms_no_recipients
		numSent = sms_no_recipients.send()
		self.assertEqual(numSent, 0)


class SMSMessageTwilioTestCase(TestCase):
	@override_settings(SMS_BACKEND='smsish.sms.backends.twilio.SMSBackend')
	def setUp(self):
		self.sms = SMSMessage(
			"Body",
			FROM_NUMBER,
			[TO_NUMBER]
		)
		self.sms_no_recipients = SMSMessage("Body", TO_NUMBER, [])

	@override_settings(SMS_BACKEND='smsish.sms.backends.twilio.SMSBackend')
	def test_create_with_subject_not_allowed(self):
		with self.assertRaises(TypeError):
			SMSMessage("Subject", "Body", FROM_NUMBER, [TO_NUMBER])

	@override_settings(SMS_BACKEND='smsish.sms.backends.twilio.SMSBackend')
	def test_recipients(self):
		sms = self.sms
		recipients = sms.recipients()
		self.assertEqual(recipients, [TO_NUMBER])

	@override_settings(SMS_BACKEND='smsish.sms.backends.twilio.SMSBackend')
	def test_send(self):
		sms = self.sms
		numSent = sms.send()
		self.assertEqual(numSent, 1)

		sms_no_recipients = self.sms_no_recipients
		numSent = sms_no_recipients.send()
		self.assertEqual(numSent, 0)


class SendSMSHelperTestCase(TestCase):
	def test_send_sms(self):
		send_sms("Body", FROM_NUMBER, [TO_NUMBER])


class SendSMSHelperTwilioTestCase(TestCase):
	@override_settings(SMS_BACKEND='smsish.sms.backends.twilio.SMSBackend')
	def test_send_sms(self):
		send_sms("Body", FROM_NUMBER, [TO_NUMBER])
