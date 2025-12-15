from data_io import IO
from quality_control import *
from normalization import *
from visualization import *

def start(
    DATA_NAME,
    QUALITY_MIN_THRESHOLD,
    MAX,
    NORMALIZE_SCALE,
    GENE_NAME,
    BINS
):
  # 1. get dafaframe (create processed data file)
  io = IO(DATA_NAME)
  df = io.get_data()

  # 2. data quality control
  df["total_expression"] = df[df.columns].sum(axis=1)

  print("\n--- Summary ---")
  print(df.describe())

  # 2-1. clean non-numeric values
  cleaned_df = clean_non_numeric(df)
  cleaned_df["total_expression"] = cleaned_df[cleaned_df.columns].drop(columns="total_expression").sum(axis=1)
  print("\n--- Total Expression ---")
  print(cleaned_df["total_expression"])

  # 2-2. clear low-quality cell data(rows) and outliers
  cleared_df = clear_low_quality_cell(cleaned_df, "total_expression", QUALITY_MIN_THRESHOLD)
  cleared_df = clear_out_range_rows(cleared_df, "total_expression", MAX)
  print("\n--- Number of Deleted Low Quality Cell ---")
  print(f"Deleted Low Quality Cell Data(Rows): {len(cleaned_df) - len(cleared_df)}")
  print(cleared_df.describe())

  # 3. normalization & stabilization
  normalized_df = normalize(cleared_df, "total_expression", NORMALIZE_SCALE)
  print("\n--- Normalized Expression Level ---")
  print(normalized_df.describe())

  stabilized_df = stabilize(normalized_df)
  print("\n--- Stabilized Expression Level ---")
  print(stabilized_df.describe())

  # save comparable data as file
  io.create_comparable_data(stabilized_df)

  # 4. visulization
  visualize_expression_level_distribution(df, "total_expression", "Total Expression per Cell (Raw Data)", BINS)
  visualize_expression_level_distribution(cleared_df, "total_expression", "Total Expression per Cell (After QC)", BINS)

  visualize_expression_level_of_gene(clear_low_quality_cell(normalized_df, GENE_NAME, 1), GENE_NAME, f"{GENE_NAME} Distribution (Before Stabilized)", BINS)
  visualize_expression_level_of_gene(clear_low_quality_cell(stabilized_df, GENE_NAME, 1), GENE_NAME, f"{GENE_NAME} Distribution (After Stabilized)", BINS)