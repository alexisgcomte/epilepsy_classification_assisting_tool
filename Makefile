.DEFAULT_GOAL := say_hello

SRC_PATH=./ecat
TEST_PATH=./tests

say_hello:
	@echo "beta version"

lint:
	flake8 $(SRC_PATH)
	flake8 $(TEST_PATH)

make test_all:
	python -m pytest

test:
	pytest -s -vvv 
	
coverage:
	pytest --cov=$(SRC_PATH) --cov-report html $(TEST_PATH) 

run:
	streamlit run $(SRC_PATH)/app.py
	