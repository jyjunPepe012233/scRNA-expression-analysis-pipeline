import pipeline

pipeline.start(
  "Bladder-10X_P4_4", # data name
  1, # quality minimum threshold
  40000, # max value limit
  10000, # normalization scale
  "Actb", # target gene name
  100 # visualization bins
)