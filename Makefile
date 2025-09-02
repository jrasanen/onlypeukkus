.PHONY: all install format build clean

all: build

install:
	uv sync

format:
	uv run ruff format onlypeukkus.py

build: install format
	uv run python onlypeukkus.py

clean:
	rm -f index.html
	rm -rf peukkus
