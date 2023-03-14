format:
	black exchangerateconversion/

lint:
	pylint exchangerateconversion/

typecheck:
	mypy exchangerateconversion/

coverage-run:
	pytest --cov=exchangerateconversion/ tests/

pre-commit: format lint typecheck coverage-run

tmp-remove: 
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf app.log
	rm -rf .coverage
	rm -rf tests/__pycache__
	rm -rf exchangerateconversion/__pycache__