clean:
	rm -rf venv

deploy:
	virtualenv -p python3 venv;     \
	. ./venv/bin/activate;     \
	python3 -m pip install -r requirements.txt;		\

run_proxy:
	. ./venv/bin/activate;     \
	python main.py -t proxy;

run_imitation:
	. ./venv/bin/activate;     \
	python main.py -t imitation;

run_decode:
	. ./venv/bin/activate;     \
	python main.py -t decode;

all: clean deploy

.DEFAULT_GOAL := all
