# OLS stats

This GitHub repository store sources (notebooks, pages) for the OLS stats

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/open-life-science/ols-program-paper/main)

## Requirements

- Install [conda](https://conda.io/miniconda.html)

    ```
    $ make install-conda
    ```

- Create the conda environment

    ```
    $ make create-env
    ```

## Explore and visualize data

Jupyter Notebooks have been used to generate the graphs for the paper. They are stored in the `src` folder


### Usage

- Launch [Jupyter](https://jupyter.org/) to access the notebooks to generate graphs

    ```
    $ make run-jupyter
    ```

- Go to [http://localhost:8888](http://localhost:8888) (a page should open automatically in your browser)
- Open the interesting notebook

    For running the microgrants & honoraria notebook, you will need first to export the output of 2 searches on CiviCRM and add them in the `data/openseeds` folder to update files
    - `data/openseeds/honorarium.csv` by "Open Seeds honorarium" search
    - `data/openseeds/microgrants.csv` by "Open Seeds microgrants" search


- Make changes and save them

## Generate website

- Run Jupyter book

    ```
    $ jupyter-book build .
    ```

- Open `_build/html/index.html` in a browser