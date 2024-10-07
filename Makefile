all: req trx

req:
	pip install -r requirements.txt

trx:
	python3 ./src/data_bank_generator.py

run-api: req
	docker build -t data_bank_generator .
	docker run -p 8000:8000 data_bank_generator
