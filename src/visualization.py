import matplotlib.pyplot as plt

def visualize_expression_level_distribution(df, total_expression_column, title, bins):
  plt.figure()
  plt.hist(df[total_expression_column], bins=bins)
  plt.title(title)
  plt.xlabel("Total Expression")
  plt.ylabel("Number of Cells")
  plt.show()

def visualize_expression_level_of_gene(df, gene_name, title, bins):
  plt.figure()
  plt.hist(df[gene_name], bins=bins)
  plt.title(title)
  plt.xlabel("Expression")
  plt.ylabel("Number of Cells")
  plt.show()