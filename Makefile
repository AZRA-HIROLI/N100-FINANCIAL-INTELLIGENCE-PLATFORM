load:
	python3 src/etl/loader.py

test:
	pytest tests/etl/ -v

clean:
	rm -f nifty100.db output/*.csv
