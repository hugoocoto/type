all: ./bin
	./bin/python3 main.py

./bin: 
	python -m venv .
