clean:
	rm -rf venv

clear_logfiles:
	rm log/*.log*

deploy:
	virtualenv -p python3 venv;     \
	. ./venv/bin/activate;     \
	python3 -m pip install -r requirements.txt;		\

run_proxy:
	. ./venv/bin/activate;     \
	python main.py -t proxy;

run_client_imitation:
	. ./venv/bin/activate;     \
	python main.py -t client_imitation;

run_full_imitation:
	. ./venv/bin/activate;     \
	python main.py -t full_imitation;

run_decode:
	. ./venv/bin/activate;     \
	python main.py -t decode;

all: clean deploy

.DEFAULT_GOAL := all
