from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.test.utils import captured_stdout
from django.test.utils import override_settings

from smsish.sms import send_sms
from smsish.sms import send_mass_sms
from smsish.sms.message import SMSMessage

VALID_FROM_NUMBER = settings.TWILIO_MAGIC_FROM_NUMBER
VALID_TO_NUMBER = settings.TWILIO_MAGIC_FROM_NUMBER


@override_settings(SMS_BACKEND='smsish.sms.backends.dummy.SMSBackend')
class SMSMessageTestCase(TestCase):
	def setUp(self):
		self.sms = SMSMessage(
			"Body",
			VALID_FROM_NUMBER,
			[VALID_TO_NUMBER]
		)
		self.sms_no_recipients = SMSMessage("Body", VALID_TO_NUMBER, [])

	def test_create_with_subject_not_allowed(self):
		with self.assertRaises(TypeError):
			SMSMessage("Subject", "Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER])

	def test_recipients(self):
		sms = self.sms
		recipients = sms.recipients()
		self.assertEqual(recipients, [VALID_TO_NUMBER])

	def test_send(self):
		sms = self.sms
		numSent = sms.send()

		# Test that one message has been sent.
		self.assertEqual(numSent, 1)
		self.assertEqual(len(mail.outbox), 0)

	def test_send_sms(self):
		numSent = send_sms("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER])
		self.assertEqual(numSent, 1)
		self.assertEqual(len(mail.outbox), 0)

	def test_send_to_nobody(self):
		sms = self.sms_no_recipients
		numSent = sms.send()

		# Test that no message has been sent.
		self.assertEqual(numSent, 0)
		self.assertEqual(len(mail.outbox), 0)

	def test_send_mass_sms(self):
		messageSpec = ("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER])
		datatuple = (messageSpec for _ in range(10))
		numSent = send_mass_sms(datatuple)
		self.assertEqual(numSent, 10)
		self.assertEqual(len(mail.outbox), 0)


@override_settings(SMS_BACKEND='smsish.sms.backends.console.SMSBackend')
class SendSMSUsingConsoleTestCase(TestCase):
	def setUp(self):
		self.sms = SMSMessage(
			"Body",
			VALID_FROM_NUMBER,
			[VALID_TO_NUMBER]
		)
		self.sms_no_recipients = SMSMessage("Body", VALID_TO_NUMBER, [])

	def test_send(self):
		with captured_stdout() as stdout:
			sms = self.sms
			numSent = sms.send()
			self.assertEqual(numSent, 1)
			output = stdout.getvalue()
			self.assertTrue("Subject: None" in output)
			self.assertTrue("From: +15005550006" in output)
			self.assertTrue("To: +15005550006" in output)
			self.assertTrue("Body" in output)

		with captured_stdout() as stdout:
			sms_no_recipients = self.sms_no_recipients
			numSent = sms_no_recipients.send()
			self.assertEqual(numSent, 0)
			self.assertEqual(stdout.getvalue(), "")

	def test_send_sms(self):
		with captured_stdout() as stdout:
			numSent = send_sms("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER])
			self.assertEqual(numSent, 1)
			self.assertEqual(len(mail.outbox), 0)
			output = stdout.getvalue()
			self.assertTrue("Subject: None" in output)
			self.assertTrue("From: +15005550006" in output)
			self.assertTrue("To: +15005550006" in output)
			self.assertTrue("Body" in output)

	def test_send_to_nobody(self):
		sms = self.sms_no_recipients
		numSent = sms.send()
		self.assertEqual(numSent, 0)
		self.assertEqual(len(mail.outbox), 0)

	def test_send_mass_sms(self):
		with captured_stdout() as stdout:
			datatuple = (("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER]) for _ in range(10))
			numSent = send_mass_sms(datatuple)
			self.assertEqual(numSent, 10)
			self.assertEqual(len(mail.outbox), 0)
			output = stdout.getvalue()
			self.assertTrue("Subject: None" in output)
			self.assertTrue("From: +15005550006" in output)
			self.assertTrue("To: +15005550006" in output)
			self.assertTrue("Body" in output)


@override_settings(SMS_BACKEND='smsish.sms.backends.twilio.SMSBackend')
class SendSMSUsingTwilioTestCase(TestCase):
	def setUp(self):
		self.sms = SMSMessage(
			"Body",
			VALID_FROM_NUMBER,
			[VALID_TO_NUMBER]
		)
		self.sms_no_recipients = SMSMessage("Body", VALID_TO_NUMBER, [])

	def test_send(self):
		sms = self.sms
		numSent = sms.send()
		self.assertEqual(numSent, 1)
		self.assertEqual(len(mail.outbox), 0)

	def test_send_sms(self):
		numSent = send_sms("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER])
		self.assertEqual(numSent, 1)
		self.assertEqual(len(mail.outbox), 0)

	def test_send_to_nobody(self):
		sms = self.sms_no_recipients
		numSent = sms.send()
		self.assertEqual(numSent, 0)
		self.assertEqual(len(mail.outbox), 0)

	def test_send_mass_sms(self):
		from smsish.sms import get_sms_connection
		with get_sms_connection(settings.SMS_BACKEND) as connection:
			datatuple = (("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER]) for _ in range(10))
			numSent = send_mass_sms(datatuple, connection=connection)
			self.assertEqual(numSent, 10)
			self.assertEqual(len(mail.outbox), 0)


@override_settings(
	SMS_BACKEND='smsish.sms.backends.filebased.SMSBackend',
	EMAIL_FILE_PATH="outbox",)
class SendSMSUsingFilebasedTestCase(TestCase):
	"""
	TODO: Test that files are actually written: see https://github.com/django/django/blob/master/tests/mail/tests.py#L876.
	"""
	def setUp(self):
		self.sms = SMSMessage(
			"Body",
			VALID_FROM_NUMBER,
			[VALID_TO_NUMBER]
		)
		self.sms_no_recipients = SMSMessage("Body", VALID_TO_NUMBER, [])

	def test_send(self):
		sms = self.sms
		numSent = sms.send()
		self.assertEqual(numSent, 1)
		self.assertEqual(len(mail.outbox), 0)

	def test_send_sms(self):
		numSent = send_sms("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER])
		self.assertEqual(numSent, 1)
		self.assertEqual(len(mail.outbox), 0)

	def test_send_to_nobody(self):
		sms = self.sms_no_recipients
		numSent = sms.send()
		self.assertEqual(numSent, 0)
		self.assertEqual(len(mail.outbox), 0)

	def test_send_mass_sms(self):
		from smsish.sms import get_sms_connection
		with get_sms_connection(settings.SMS_BACKEND) as connection:
			datatuple = (("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER]) for _ in range(10))
			numSent = send_mass_sms(datatuple, connection=connection)
			self.assertEqual(numSent, 10)
			self.assertEqual(len(mail.outbox), 0)


@override_settings(SMS_BACKEND='smsish.sms.backends.locmem.SMSBackend')
class SendSMSUsingLocmemTestCase(TestCase):
	def setUp(self):
		self.sms = SMSMessage(
			"Body",
			VALID_FROM_NUMBER,
			[VALID_TO_NUMBER]
		)
		self.sms_no_recipients = SMSMessage("Body", VALID_TO_NUMBER, [])

	def test_send(self):
		sms = self.sms
		numSent = sms.send()
		self.assertEqual(numSent, 1)
		self.assertEqual(len(mail.outbox), 1)

	def test_send_sms(self):
		numSent = send_sms("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER])
		self.assertEqual(numSent, 1)
		self.assertEqual(len(mail.outbox), 1)

	def test_send_to_nobody(self):
		sms = self.sms_no_recipients
		numSent = sms.send()
		self.assertEqual(numSent, 0)
		self.assertEqual(len(mail.outbox), 0)

	def test_send_mass_sms(self):
		from django.conf import settings
		from smsish.sms import get_sms_connection
		with get_sms_connection(settings.SMS_BACKEND) as connection:
			datatuple = (("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER]) for _ in range(10))
			numSent = send_mass_sms(datatuple, connection=connection)
			self.assertEqual(numSent, 10)
			self.assertEqual(len(mail.outbox), 10)


@override_settings(SMS_BACKEND='smsish.sms.backends.rq.SMSBackend')
@override_settings(SMSISH_RQ_SMS_BACKEND='smsish.sms.backends.locmem.SMSBackend')
@override_settings(TESTING=True)
class SendSMSUsingRQTestCase(TestCase):
	def setUp(self):
		self.sms_no_recipients = SMSMessage("Body", VALID_TO_NUMBER, [])

	def get_new_sms_message(self):
		return SMSMessage(
			"Body",
			VALID_FROM_NUMBER,
			[VALID_TO_NUMBER]
		)

	def test_send(self):
		with self.assertRaises(AssertionError):
			sms = self.get_new_sms_message()
			numSent = sms.send()
			self.assertEqual(numSent, 1)
			self.assertEqual(len(mail.outbox), 1)

	def process_jobs(self):
		from django_rq import get_worker
		get_worker().work(burst=True)

	def test_send_with_connection(self):
		# from django.conf import settings
		from smsish.sms import get_sms_connection
		sms = self.get_new_sms_message()
		with get_sms_connection() as connection:
			jobs = connection.send_messages([sms])
			self.assertEqual(len(jobs), 1)
			# http://python-rq.org/docs/testing/
			# https://github.com/ui/django-rq#testing-tip
			self.assertEqual(len(mail.outbox), 1)
			self.process_jobs()
			for job in jobs:
				self.assertTrue(job.id)
				self.assertEqual(job.args[0].body, sms.body)

	def test_send_sms(self):
		with self.assertRaises(AssertionError):
			numSent = send_sms("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER])
			self.assertEqual(numSent, 1)
			self.assertEqual(len(mail.outbox), 1)

	def test_send_to_nobody(self):
		sms = self.sms_no_recipients
		numSent = sms.send()
		self.assertEqual(numSent, 0)
		self.assertEqual(len(mail.outbox), 0)

	def test_send_mass_sms(self):
		from django.conf import settings
		from smsish.sms import get_sms_connection
		with self.assertRaises(NotImplementedError):
			with get_sms_connection(settings.SMS_BACKEND) as connection:
				datatuple = (("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER]) for _ in range(10))
				numSent = send_mass_sms(datatuple, connection=connection)
				self.assertEqual(numSent, 10)
				self.assertEqual(len(mail.outbox), 0)


TEST_SMTP_BACKENDS = False
if TEST_SMTP_BACKENDS:
	@override_settings(
		SMS_BACKEND='smsish.sms.backends.smtp.SMSBackend',
		EMAIL_HOST="127.0.0.1",
		EMAIL_PORT=1025,
		EMAIL_HOST_USER="",
		EMAIL_HOST_PASSWORD="",
		EMAIL_USE_TLS=False,)
	class SendSMSUsingSMTPTestCase(TestCase):
		def setUp(self):
			self.sms = SMSMessage(
				"Body",
				VALID_FROM_NUMBER,
				[VALID_TO_NUMBER]
			)
			self.sms_no_recipients = SMSMessage("Body", VALID_TO_NUMBER, [])

		def test_send(self):
			sms = self.sms
			numSent = sms.send()
			self.assertEqual(numSent, 1)

		def test_send_sms(self):
			numSent = send_sms("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER])
			self.assertEqual(numSent, 1)

		def test_send_to_nobody(self):
			sms = self.sms_no_recipients
			numSent = sms.send()
			self.assertEqual(numSent, 0)
			self.assertEqual(len(mail.outbox), 0)

		def test_send_mass_sms(self):
			with captured_stdout() as stdout:
				datatuple = (("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER]) for _ in range(10))
				numSent = send_mass_sms(datatuple)
				self.assertEqual(numSent, 10)
				self.assertEqual(len(mail.outbox), 0)
				output = stdout.getvalue()
				self.assertTrue("Subject: None" in output)
				self.assertTrue("From: +15005550006" in output)
				self.assertTrue("To: +15005550006" in output)
				self.assertTrue("Body" in output)

	@override_settings(SMS_BACKEND='smsish.sms.backends.mailcatcher.SMSBackend')
	class SendSMSUsingMailCatcherTestCase(TestCase):
		def setUp(self):
			self.sms = SMSMessage(
				"Body",
				VALID_FROM_NUMBER,
				[VALID_TO_NUMBER]
			)
			self.sms_no_recipients = SMSMessage("Body", VALID_TO_NUMBER, [])

		def test_send(self):
			sms = self.sms
			numSent = sms.send()
			self.assertEqual(numSent, 1)

		def test_send_sms(self):
			numSent = send_sms("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER])
			self.assertEqual(numSent, 1)

		def test_send_to_nobody(self):
			sms = self.sms_no_recipients
			numSent = sms.send()
			self.assertEqual(numSent, 0)
			self.assertEqual(len(mail.outbox), 0)

		def test_send_mass_sms(self):
			with captured_stdout() as stdout:
				datatuple = (("Body", VALID_FROM_NUMBER, [VALID_TO_NUMBER]) for _ in range(10))
				numSent = send_mass_sms(datatuple)
				self.assertEqual(numSent, 10)
				self.assertEqual(len(mail.outbox), 0)
				output = stdout.getvalue()
				self.assertTrue("Subject: None" in output)
				self.assertTrue("From: +15005550006" in output)
				self.assertTrue("To: +15005550006" in output)
				self.assertTrue("Body" in output)
