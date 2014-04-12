
calculate_sample_data <- function(init,end) {
  sample <- data_matrix[init:end,]    
  mainDir <- "/mnt/sdb1/tweeprofiles/R_Project_server"  
  subDir <- toString(init - 1)
  setwd(file.path(mainDir, subDir))
  saveRDS(sample, file = "sample.rds")
}

# Create matrices for overlapped subsets
init <- 1
inc <- 7500
while(init + inc <= dim+1){  
  end <- init + inc - 1
  calculate_sample_data(init,end)
  init <- init  + inc/2
}
