.PHONY: run
run:
	streamlit run supervised/main.py --server.runOnSave true

.PHONY: backend
backend:
	streamlit run supervised/backend.py --server.runOnSave true
