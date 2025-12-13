import pandas as pd
import numpy as np

def normalize(df, total_expression_column, scale):
  norm = df.div(df[total_expression_column], axis=0) * scale
  return norm

def stabilize(df):
  return np.log1p(df)