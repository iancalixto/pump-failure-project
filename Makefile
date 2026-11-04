.PHONY: install test kernel clean pdf

install:
	pip install -e ".[dev]"

kernel:
	python -m ipykernel install --user --name pumpfail --display-name "Python (pumpfail)"

test:
	python -m pytest -q

pdf:
	typst compile docs/DEFENSE_AND_STUDY_GUIDE.typ docs/DEFENSE_AND_STUDY_GUIDE.pdf

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
