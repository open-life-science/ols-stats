# Settings
CONDA_ENV=ols-program-paper
SHELL=bash

CONDA=$(shell which conda)
ifeq ($(CONDA),)
	CONDA=${HOME}/miniconda3/bin/conda
endif

default: help

build-paper: paper.pdf ## build paper
.PHONY: build-paper

paper.pdf:
	latexmk -pdf paper.tex

clean-paper: ## clean paper
	latexmk -C
.PHONY: clean-paper

install-conda: ## install Miniconda
	curl -L $(MINICONDA_URL) -o miniconda.sh
	bash miniconda.sh -b
.PHONY: install-conda

create-env: ## create conda environment
	if ${CONDA} env list | grep '^${CONDA_ENV}'; then \
	    ${CONDA} env update -f environment.yml; \
	else \
	    ${CONDA} env create -f environment.yml; \
	fi
.PHONY: create-env

ACTIVATE_ENV = source $(shell dirname $(dir $(CONDA)))/bin/activate $(CONDA_ENV)

run-jupyter: ## run jupyter notebooks
	$(ACTIVATE_ENV) && \
		jupyter notebook

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
