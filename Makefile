.PHONY: run
run:
	streamlit run supervised/main.py --server.runOnSave true

.PHONY: backend
backend:
	python supervised/backend.py
