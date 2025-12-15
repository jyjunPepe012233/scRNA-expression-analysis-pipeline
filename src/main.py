import pipeline

pipeline.start(
  "Spleen-10X_P7_6", # data name
  10, # quality minimum threshold
  20000, # max value limit
  10000, # normalization scale
  "Actb", # target gene name
  300 # visualization bins
)