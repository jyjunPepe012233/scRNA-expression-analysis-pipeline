# Overview

This project is a program for analyzing single-cell RNA expression data.

It was developed by applying the concepts and workflow learned from the
[single-cell-pipeline](https://github.com/jyjunPepe012233/single-cell-pipeline) repository,
which focuses on understanding the step-by-step structure of single-cell data analysis.

### Raw Data vs After QC (Total Expression per Cell)

<p align='left'>
  <img width=40% alt="visualization_b_raw" src="./images/01_total_expression_per_cell_raw_data.png"/>
  <img width=40% alt="visualization_b_raw" src="./images/02_total_expression_per_cell_after_qc.png"/>
</p>

### Raw Data vs After Processing (Expression Distribution of Specific RNA)
<p align='left'>
  <img width=40% alt="visualization_b_raw" src="./images/03_total_expression_per_cell_before_stabilized.png"/>
  <img width=40% alt="visualization_b_raw" src="./images/04_total_expression_per_cell_after_stabilized.png"/>
</p>

# Project Structure

```
scRNA-expression-analysis-pipeline
├── data
│   ├── comparable
│   │   └── Bladder-10X_P4_4
│   │       └── comparable_Bladder-10X_P4_4.csv
│   ├── processed
│   │   └── Bladder-10X_P4_4
│   │       └── processed_Bladder-10X_P4_4.csv
│   └── raw
│       ├── Bladder-10X_P4_3
│       │   ├── barcodes.tsv
│       │   ├── genes.tsv
│       │   └── matrix.mtx
│       ├── Bladder-10X_P4_4
│       ├── Heart-10X_P7_4
│       └── ...
├── images
└── src
    ├── data_io.py
    ├── main.py
    ├── normalization.py
    ├── pipeline.py
    ├── quality_control.py
    └── visualization.py
```

# Key Features

- Up to 28 datasets can be analyzed and visualized by adjusting parameters in `/src/main.py`
- Supports scRNA-seq datasets based on .mtx and .tsv files
- Implements a full preprocessing workflow: Data loading, Quality control, Normalization and Stabilization, Visualization
- Provides: Cell-level total expression histograms, Gene-level expression distribution histograms

# Step 1. Data Loading & Validation

The `/src/data_io.py` module parses expression matrix data into a DataFrame.

It provides the following functionality:

- Converts .mtx and .tsv-based datasets into a single .csv file
- Automatically reuses converted .csv files to avoid redundant processing (caching)
- Saves processed files again for record-keeping and reproducibility

This design was implemented with real research environments in mind,
where data reuse and traceability are important.

# Step 2. Quality Control (QC)

Not all cells are suitable for analysis.

During exploration, cells with zero total RNA expression were observed.
Such cells were considered likely to be:
- dead cells, or
- cells affected by technical issues during capture or sequencing

Cells below a user-defined quality minimum threshold, specified at the program entry point,
are treated as low-quality cells and excluded from further analysis.

Additional filtering conditions can also be configured at the entry point
to flexibly adjust analysis criteria depending on the dataset.

The `/src/schema.py` module provides the following functionality:
- Converts non-numeric values to NaN
- Removes low-quality cells based on total expression thresholds

Filters out extreme outliers with abnormally high total expression

# Step 3. Normalization

Due to differences in sequencing depth and other technical factors,
total expression levels may not accurately reflect biological proportions.

To address this and enable meaningful comparison of relative gene expression,
the pipeline applies normalization.

The `/src/normalization.py` module provides:

- Library-size normalization: Each cell is scaled to the same total expression level (configurable, default = 10,000)
- log1p transformation: Stabilizes the distribution and reduces the impact of extreme values

The normalized and stabilized data are saved as .csv files in the
`/data/comparable/` directory.

Step 4. Visualization & Validation

Visualization is used as a validation tool, not for presentation purposes.

The `/src/visualization.py` module provides visualizations that allow verification of preprocessing decisions.
Example outputs can be found in the `/images/ directory`.

Supported visualizations include:
- Cell-level total expression histograms (before and after QC)
- Gene-level expression distribution comparisons (before and after processing)

Through these visualizations, it is possible to confirm:
- whether low-quality cells and outliers were effectively removed
- how normalization and stabilization changed expression distributions
