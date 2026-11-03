.PHONY: install test kernel clean

install:
	pip install -e ".[dev]"

kernel:
	python -m ipykernel install --user --name pumpfail --display-name "Python (pumpfail)"

test:
	python -m pytest -q

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +