RENDER_FILE = sample.py

.PHONY: init activate prev clean

SHELL := /bin/bash

init:
	uv sync

prev:
	. .venv/bin/activate && manim render -p -q l $(RENDER_FILE)

clean:
	rm -rf media