.PHONY: clean test coverage covhtml

# Clean pyc and __pycache__
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	echo "Cleaned __pycache__ and .pyc files."

# Run pytest only
test:
	pytest --ds=config.settings

# Run pytest with coverage
coverage:
	pytest --ds=config.settings --cov=plan_it --cov-report=term-missing --cov-report=html

# Open the HTML coverage report (Linux/Mac)
covhtml:
	xdg-open htmlcov/index.html || open htmlcov/index.html || echo "Please open htmlcov/index.html manually."
