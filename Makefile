.PHONY: test lint security demo notebook

test:
	python -m pytest

lint:
	ruff check .
	python -m compileall -q aegis apps redteam security_agents evaluation integrations observability tests

security:
	bandit -q -r aegis apps redteam security_agents evaluation
	pip-audit

demo:
	python examples/run_demo.py

notebook:
	python -m nbconvert --to notebook --execute notebooks/aegis_pipeline_demo.ipynb --output-dir output/jupyter-notebook --output aegis_pipeline_demo.executed.ipynb