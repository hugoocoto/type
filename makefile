run: ./bin
	./bin/python3 main.py

./bin: 
	python -m venv .

install: ./bin
	pyinstaller --onefile --distpath . main.py -n type \
		--add-data "english10k.wordlist:."
