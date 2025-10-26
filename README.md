# 🧭 Project Setup Guide – NextDate

## 1. Environment Preparation

To ensure consistency and isolated dependencies, use **pyenv** and **pipenv**.

```bash
# Install pyenv (for managing Python versions)
curl https://pyenv.run | bash
exec "$SHELL"

# Install a compatible Python version (example: 3.12)
pyenv install 3.12.4
pyenv local 3.12.4

# Install pipenv
pip install pipenv

2. Create and Activate the Virtual Environment
# Create a virtual environment with development dependencies
pipenv install --dev

# Activate it
pipenv shell

3. Run Tests and Coverage
# Run all unit tests
pytest -q

# Run tests with coverage report
pytest --cov=next_date --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=next_date --cov-report=html


To open the coverage report:

xdg-open htmlcov/index.html

Test Coverage Report Summary

(From the official report document)

Field	Details
Report Title	Test Coverage Report – NextDate Class
Prepared By	Yasin Türk, Toprak Zeybek
Reviewed By	Tuğkan Tuğlular
Approved By	IZTECH
Date	26.10.2025
Test Techniques Used

Equivalence Class Testing (ECT)

Decision Table Testing (DTT)

Boundary Value Testing (BVT)

Key Metrics
Area	Coverage
Functional Testing	94%
Integration Testing	100%
System Testing	100%
Overall	96%
Findings

The deliberate bug in last_business_day_of_month() was successfully detected by BVT, ECT, and DTT test suites.

Weak oracle tests failed to catch the bug, highlighting the need for stronger assertion logic.

Overall code coverage reached 96%.

Next Steps

Fix the condition:

while cur.weekday() > 5:  # → should be >= 5

Re-run tests to confirm 100% coverage.

Add more edge-case validations for boundary years (1812–2012).