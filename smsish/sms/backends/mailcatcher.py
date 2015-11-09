from .smtp import SMSBackend as SMTPSMSBackend


class SMSBackend(SMTPSMSBackend):
	def __init__(self, *args, **kwargs):
		super(SMSBackend, self).__init__(host="127.0.0.1", port=1025, username="", password="")
