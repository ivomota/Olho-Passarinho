# Calculates the geodesic distance between two points specified by radian latitude/longitude using the
# Haversine formula (hf) (http://www.r-bloggers.com/great-circle-distance-calculations-in-r/)
hf <- function(long1, lat1, long2, lat2) {
  R <- 6371 # Earth mean radius [km]
  delta.long <- (long2 - long1)
  delta.lat <- (lat2 - lat1)
  a <- sin(delta.lat/2)^2 + cos(lat1) * cos(lat2) * sin(delta.long/2)^2
  c <- 2 * asin(min(1,sqrt(a)))
  d = R * c
  return(d) # Distance in km
}

# Convert degrees to radians
deg2rad <- function(deg) return(deg*pi/180)

# Calculate all dissimilarity matrices (spatial, temporal, content) raw and normalized
# for a given subset with indexes in interval [init,end]
calculate_spatial_distance <- function(init,end) {
  sample <- data_matrix[init:end,]
  sample_sp_dist <- matrix(0,dim(sample)[1],dim(sample)[1]) 
  #Normalized variables (between 0 and 1)
  #formula: x[i,j] / max  
  
  mainDir <- "/mnt/sdb1/tweeprofiles/R_Project_server"  
  
  #Spatial Matrix
  for(i in 1:dim(sample)[1]){
    for(j in 1:dim(sample)[1]){
      sample_sp_dist[i,j] = hf(deg2rad(as.numeric(sample[i,5])),
                               deg2rad(as.numeric(sample[i,6])),
                               deg2rad(as.numeric(sample[j,5])),
                               deg2rad(as.numeric(sample[j,6])))
    }
  }
  rm(i,j)
  
  subDir <- toString(init - 1)
  dir.create(file.path(mainDir, subDir), showWarnings = FALSE)
  setwd(file.path(mainDir, subDir))
  saveRDS(sample_sp_dist, file = "sample_sp_dist.rds")
  
  rm(sample_sp_dist)
}

#Calculate subsets
init <- 1
inc <- 7500
while(init + inc <= dim+1){  
  end <- init + inc - 1
  calculate_spatial_distance(init,end)
  init <- init  + inc/2
}