init:
	pip3 install -r requirements.txt

update:
	pip install pykrx --upgrade

test:
	nosetests tests