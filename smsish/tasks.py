import django_rq
from rq.decorators import job

DEFAULT_QUEUE_NAME = "default"
DEFAULT_REDIS_CONNECTION = django_rq.get_connection()


@job(DEFAULT_QUEUE_NAME, connection=DEFAULT_REDIS_CONNECTION)
def send_sms(*args, **kwargs):
	from smsish.sms import send_sms as _send_sms
	return _send_sms(*args, **kwargs)


@job(DEFAULT_QUEUE_NAME, connection=DEFAULT_REDIS_CONNECTION)
def send_mass_sms(*args, **kwargs):
	from smsish.sms import send_mass_sms as _send_mass_sms
	return _send_mass_sms(*args, **kwargs)
