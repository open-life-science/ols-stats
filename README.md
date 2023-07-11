# OLS program paper

This GitHub repository store sources (scripts, data, images) for the OLS program paper.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/open-life-science/ols-program-paper/main)

## Structure of the repository

Folders:
- `data` with CSVs containing the data
- `images` with images generated from the data, and also sources (SVG) for any images in the paper
- `src` with scripts and Jupyter Notebooks used to get, explore, analyze and visualize data

## Requirements

- Install [conda](https://conda.io/miniconda.html)

    ```
    $ make install-conda
    ```

- Create the conda environment

    ```
    $ make create-env
    ```



## Extract and format data

Data from the OLS website is automatically extracted **every week** and then formatted to be stored as CSV files in the `data` folder and really to be explored and visualized.

To run the data extraction and formatting manually

- Generate a Personal access token on GitHub (Settings - Developer settings - Personal access token ) and copy it to [`config.yml` file](config.yaml)
- Run

    ```
    $ python src/extract_data_from_website.py --token <TOKEN> --out data
    ```

## Explore and visualize data

Jupyter Notebooks have been used to generate the graphs for the paper. They are stored in the `src` folder

- [`src/extract_data_from_website.ipynb`](src/extract_data_from_website.ipynb): Extract information from the website to create CSVs in `data` folder


Usage

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