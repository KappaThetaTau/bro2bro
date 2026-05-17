.PHONY: setup run clean

# Define a variable for the virtual environment directory
VENV_DIR = .venv

setup:
	@echo "Setting up virtual environment and installing dependencies..."
	python -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements.txt

run:
	@echo "Running the interview scheduler program..."
	$(VENV_DIR)/bin/python main.py

clean:
	@echo "Cleaning up virtual environment and build artifacts..."
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -r {} +