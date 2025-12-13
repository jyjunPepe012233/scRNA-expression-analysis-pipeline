import pandas as pd

def clean_non_numeric(df):
    target = df.copy()
    coerced = target.apply(pd.to_numeric, errors="coerce")
    target.loc[:, :] = coerced
    return target

def clear_low_quality_cell(df, total_expression_column, threshold):
    cleared = df[df[total_expression_column] >= threshold]
    return cleared

def clear_out_range_rows(df, total_expression_column, max):
    cleared = df[df[total_expression_column] < max]
    return cleared