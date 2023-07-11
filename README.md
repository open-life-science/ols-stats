# OLS program paper

This GitHub repository store sources (scripts, data, images) for the OLS program paper.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/open-life-science/ols-program-paper/main)

## Structure of the repository

Folders:
- `data` with CSVs containing the data
- `images` with images generated from the data, and also sources (SVG) for any images in the paper
- `src` with Jupyter Notebooks used to get, explore, analyze and visualize data

## Generation of graphs for the paper

Jupyter Notebooks have been used to generate the graphs for the paper. They are stored in the `src` folder

- [`src/extract_data_from_website.ipynb`](src/extract_data_from_website.ipynb): Extract information from the website to create CSVs in `data` folder

### Requirements

- Install [conda](https://conda.io/miniconda.html)

    ```
    $ make install-conda
    ```

- Create the conda environment

    ```
    $ make create-env
    ```

- (Only for ) Generate a Personal access token on GitHub (Settings - Developer settings - Personal access token ) and copy it to [`config.yml` file](config.yaml)

### Usage

- Launch [Jupyter](https://jupyter.org/) to access the notebooks to generate graphs

    ```
    $ make run-jupyter
    ```

- Go to [http://localhost:8888](http://localhost:8888) (a page should open automatically in your browser)
- Open the interesting notebook
- Make changes and save them
- Generate HTML for website

    In Jupyter:

    - Create a new terminal
    - Run

        ```
        $ quarto render src/<notebook> --to html
        ```

    - Move the generated files into `docs`