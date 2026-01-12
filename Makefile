.PHONY: run build-books check-ref test

run:
	python -m streamlit run app/main.py

build-books:
	python scripts/build_book_embeddings.py

check-ref:
	python scripts/sanity_check_referential.py

test:
	python -m unittest discover tests
