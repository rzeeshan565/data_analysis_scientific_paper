# Research Citation Analysis

This project analyzes citation patterns in IoT conference papers using Python. It includes data preprocessing, feature engineering, and generation of publication-ready visualizations.

## Prerequisites

- Python 3.8 or higher
- `pip` installed
- Git (optional, if cloning)

## Clone or Download the Repository
* git@github.com:rzeeshan565/data_analysis_scientific_paper.git

## Set Up Virtual Environment

**1. Create a virtual environment named `myenv`:**
* python -m venv myenv

## Create and Activate Virtual Environment
* python -m venv myenv

### On macOS/Linux:
* source myenv/bin/activate

### On Windows:
* .\myenv\Scripts\activate


## Install Required Dependencies
* pip install -r requirements.txt


## Run the Analysis
* Make sure the virtual environment is activated.
* Then run: 
* python scripts/citation_analysis.py

## This will:
* Load the Excel dataset
* Preprocess and encode features
* Compute correlations
* Export a clean PDF plot to /results/
* (Optional: needs uncommenting print statements) Print top conference and country correlations to console
