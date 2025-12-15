from pathlib import Path
from scipy.io import mmread
import pandas as pd

PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent

class IO:
  def __init__(self, data_name: str):
    self.data_name = data_name
    self.data_path = self.get_path_by_data_type("raw")
    # load dataframe when processed data already exists
    processed_data_path = self.get_path_by_data_type("processed")
    processed_data_file = processed_data_path / self.get_file_name_by_data_type("processed")
    if (processed_data_path.exists() and processed_data_file.exists()):
      print("Processed data is already exists. Will not be made new processed data.")
      self.data = pd.read_csv(processed_data_file, index_col=0)
    else:
      self.data = None
  
  def get_path_by_data_type(self, data_type):
    return (PROJECT_ROOT_DIR / "data" / data_type / self.data_name).resolve()
  
  def get_file_name_by_data_type(self, data_type):
    return f"{data_type}_{self.data_name}.csv"
  
  def __save(self, df, data_type):
    path = self.get_path_by_data_type(data_type)
    path.mkdir(exist_ok=True)
    file = path / self.get_file_name_by_data_type(data_type)
    print("Try to save new file as" + str(file))
    df.to_csv(file)
    print("New data saved!")
  
  def get_data(self):
    if (self.data is None):
      self.data = self.create_processed_data()
    return self.data.transpose()
  
  def create_processed_data(self): 
    try:
      # 1. read matrix
      matrix = mmread(self.data_path / "matrix.mtx")   # sparse matrix

      # 2. read gene and cell names
      genes = pd.read_csv(str(self.data_path) + "/genes.tsv", sep="\t", header=None)[0].values
      cells = pd.read_csv(str(self.data_path) + "/barcodes.tsv", sep="\t", header=None)[0].values

      # 3. convert to dataframe
      df = pd.DataFrame(matrix.toarray(), index=genes, columns=cells)

      # 4. save as temp
      self.__save(df, "processed")
      return df
    except:
      raise

  def create_comparable_data(self, df):
    self.__save(df.transpose(), "comparable")