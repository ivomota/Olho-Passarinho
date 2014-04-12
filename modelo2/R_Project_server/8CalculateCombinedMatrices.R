calculate_combined_matrix<- function(subset,w1,w2,w3,w4)
{  
  mainDir <- "/mnt/sdb1/tweeprofiles/R_Project_server"  
  subDir <- toString(subset)
  setwd(file.path(mainDir, subDir))
  
  sample_sp_dist_norm <- readRDS("sample_sp_dist_norm.rds")
  sample_tp_dist_norm <- readRDS("sample_tp_dist_norm.rds")
  sample_ct_dist <- readRDS("sample_ct_dist_norm.rds")
  sample_so_dist_norm <- readRDS("sample_so_dist_norm.rds")
  
  combined_matrix <- matrix(0,dim(sample_sp_dist_norm)[1],dim(sample_sp_dist_norm)[1])
  
  for(i in 1:dim(combined_matrix)[1]){
    for(j in 1:dim(combined_matrix)[1]){
      combined_matrix[i,j] =   w1 * sample_sp_dist_norm[i,j] + 
        w2 * sample_tp_dist_norm[i,j] + 
        w3 * sample_ct_dist[i,j] +
        w4 * sample_so_dist_norm[i,j]
    }
  }
  rm(i,j)
  
  mainDir <- str_replace_all(paste("/mnt/sdb1/tweeprofiles/R_Project_server/", subDir), " ", "")
  subDir <- "combined_matrices"
  dir.create(file.path(mainDir, subDir), showWarnings = FALSE)
  setwd(file.path(mainDir, subDir))
  x <- c("combined_matrix_", w1, "_", w2, "_",w3, "_",w4, ".rds")
  y <- str_replace_all(toString(x), ", ", "")
  saveRDS(combined_matrix, file = y)
  
  rm(combined_matrix, sample_sp_dist_norm, sample_tp_dist_norm, sample_ct_dist, sample_so_dist_norm)
}

vars <- read.csv(file="/mnt/sdb1/tweeprofiles/R_Project_server/vars.csv", sep=";", header=F)

subset <- 65000
inc <- 7500
while(subset + inc <= 120000){  
  for(i in 1:dim(vars)[1]){
    w1 <- as.numeric(vars[i,1])
    w2 <- as.numeric(vars[i,2])
    w3 <- as.numeric(vars[i,3])
    w4 <- as.numeric(vars[i,4])
    calculate_combined_matrix(subset,w1,w2,w3,w4)
    print(i)
  }
  
  subset <- subset  + inc/2
}
