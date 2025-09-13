run: ./bin
	./bin/python3 main.py

./bin: 
	python -m venv .

install: ./bin
	pyinstaller --onefile --distpath . main.py
