.DEFAULT_GOAL := say_hello

SRC_PATH=./epilepsy_classification_assisting_tool
TEST_PATH=./tests

say_hello:
	@echo "beta version"

lint:
	flake8 $(SRC_PATH)
	flake8 $(TEST_PATH)


make test_all:
	python -m pytest

test:
	pytest -s -vvv $(TEST_PATH)
	
coverage:
	pytest --cov=epilepsy_classification_assisting_tool/ --cov-report html tests/ 

run:
	streamlit run ./epilepsy_classification_assisting_tool/app.py
