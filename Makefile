test:
	coverage run --branch --source=uploadstatic `which django-admin.py` test --settings=uploadstatic.test_settings uploadstatic
	coverage report --omit=uploadstatic/test*
