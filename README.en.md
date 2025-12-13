# scRNA Expression Analysis Pipeline

[![ko](https://img.shields.io/badge/lang-한국어-blue.svg)](README.ko.md)

# Overview

This project is a **preprocessing and validation pipeline designed to transform raw scRNA-seq data into an analyzable state**.

In single-cell RNA expression analysis, this project aims to understand:

* why raw scRNA-seq data cannot be analyzed directly, and
* what kinds of decisions and transformations are required to make the data suitable for analysis.

The pipeline was developed based on the **four-step data processing workflow and analytical mindset** learned from the
[`single-cell-pipeline`](https://github.com/jyjunPepe012233/single-cell-pipeline) repository,
and was extended to **directly handle raw scRNA-seq data (.mtx, .tsv) as input**.

# Learning Motivation

To design this pipeline, I began by asking the following questions:

* **Why can’t raw scRNA-seq data be analyzed directly?**
* What does *cell quality* mean, and **how does removing low-quality cells change the dataset?**
* When measuring gene expression per cell, **what is the purpose of normalization?**
* When examining gene expression distributions, **why is log-based stabilization necessary?**

Through these questions, I gradually built my understanding of single-cell analysis and
experienced the practical challenges involved in real data preprocessing and validation.

# What This Pipeline Does

* Loads raw scRNA-seq data (.mtx, .tsv) (`/src/data_io.py`)
* Performs cell-level quality control (`/src/schema.py`)
* Applies library-size normalization and log-based stabilization (`/src/normalization.py`)
* Validates preprocessing decisions through before/after distribution comparisons (`/src/visualization.py`)

Rather than focusing on reproducing every detail of real research environments,
this project emphasizes **directly experiencing the core problems encountered during analysis**
and documenting my own solutions and reasoning as a way to move closer to bioinformatics practice.

# Analysis Pipeline

## Step 1. Data Loading & Structural Validation

Real scRNA-seq datasets obtained from public sources were used.

A module was implemented to convert mtx-based datasets into a DataFrame structure,
allowing further inspection and processing.

## Step 2. Quality Control (QC)

Using `describe()`, I observed that many cells had a total RNA expression value of zero.

These cells were considered likely to be:

* cells that failed during capture or sequencing, or
* dead cells with no meaningful RNA expression.

Cells with total expression below a specified threshold were therefore excluded from analysis.

Since different datasets have different value ranges and characteristics,
the program allows configuration of parameters such as:

* minimum quality threshold (`quality_min_threshold`)
* outlier cutoff (`max_value_limit`)

These parameters can be adjusted at the program entry point.

### Raw Data vs After QC (Total Expression per Cell)

<p align='left'>
  <img width=40% src="./images/01_total_expression_per_cell_raw_data.png"/>
  <img width=40% src="./images/02_total_expression_per_cell_after_qc.png"/>
</p>

## Step 3. Normalization & Stabilization

Raw scRNA-seq data often shows large differences in total expression per cell
due to variations in sequencing depth and technical factors.

Comparing gene expression values without addressing this issue is not meaningful.
Therefore, before comparison:

* each cell’s total expression was normalized to the same scale
  (default: 10,000, configurable), and
* expression distributions were stabilized using NumPy’s `log1p` function.

This stabilization allows relative differences in gene expression
to be compared on a more interpretable scale.

### Raw Data vs After Processing (Expression Distribution of a Representative Gene)

<p align='left'>
  <img width=40% src="./images/03_total_expression_per_cell_before_stabilized.png"/>
  <img width=40% src="./images/04_total_expression_per_cell_after_stabilized.png"/>
</p>

## Step 4. Visualization

To verify that the QC and normalization steps had meaningful effects,
the data was visualized and compared before and after preprocessing.

The following visualizations are provided and saved in the `/images/` directory:

* cell-level total expression distributions (before / after QC)
* gene-level expression distributions (before / after full processing)

# What I Learned

Through this project, I was able to answer the following questions:

* **Why can’t raw scRNA-seq data be analyzed directly?**
  Raw measurement data often contains missing values, outliers, and inconsistent structures.
  Preprocessing is necessary to ensure data reliability and comparability.

* What does *cell quality* mean, and **how does removing low-quality cells change the data?**
  Cells with zero RNA expression, often caused by capture or sequencing failures,
  do not provide meaningful information and should be excluded.
  Removing such cells enables more reliable comparisons across the dataset.

* When measuring gene expression per cell, **why is normalization necessary?**
  Differences in sequencing depth lead to different total expression scales per cell.
  Without normalization, relative gene expression differences cannot be compared meaningfully.

* When analyzing gene expression distributions, **why is log-based stabilization needed?**
  Extreme values can dominate the distribution and obscure relative differences.
  Log-based stabilization reduces this effect and makes expression patterns easier to interpret.
