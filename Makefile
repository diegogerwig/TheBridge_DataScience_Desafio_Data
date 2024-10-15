all: trx

req: 
	pip install -r requirements.txt

trx: req
	python3 ./src/main.py

predict: req
	python3 ./src/prediction_30_days.py
	python3 ./src/alert_trx.py

api: req
	docker build -t data_bank_generator .
	docker run -p 8000:8000 data_bank_generator
