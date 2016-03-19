clean:
	rm -rf ./build ./dist

init:
	pip install -r requirements.txt

test:
	python manage.py test smsish

build:
	python setup.py sdist
