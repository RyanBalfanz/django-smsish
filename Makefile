clean:
	rm -rf ./build ./dist ./htmlcov/

coverage_report: test_coverage
	coverage report -m
	coverage html

init:
	pip install -r requirements.txt

test:
	python manage.py test smsish

test_coverage:
	coverage run manage.py test smsish

build:
	python setup.py sdist
