#Temporal distance function
tp_dist_function <- function(t1,t2) {
  return(abs(difftime(t1, t2, units='secs'))) #time interval
}

calculate_temporal_distances <- function(init,end) {
  sample <- data_matrix[init:end,]
  sample_tp_dist <- matrix(0,dim(sample)[1],dim(sample)[1]) 
  #Normalized variables (between 0 and 1)
  #formula: x[i,j] / max  
  
  mainDir <- "/mnt/sdb1/tweeprofiles/R_Project_server"  
  subDir <- toString(init - 1)
  
  #Temporal Matrix
  for(i in 0:dim(sample)[1]){ 
    for(j in 0:dim(sample)[1]){
      sample_tp_dist[i,j] = tp_dist_function(sample[i,4], sample[j,4])      
    }
  }
  rm(i,j)
  
  
  setwd(file.path(mainDir, subDir))
  saveRDS(sample_tp_dist, file = "sample_tp_dist.rds")
  
  rm(sample_tp_dist)
}

# Create matrices for overlapped subsets
init <- 1
inc <- 7500
while(init + inc <= dim+1){  
  end <- init + inc - 1
  calculate_temporal_distances(init,end)
  init <- init  + inc/2
}

