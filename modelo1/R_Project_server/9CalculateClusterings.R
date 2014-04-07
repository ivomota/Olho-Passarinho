library("fpc")


calculate_clustering_dbscan<- function(subset) 
{  
  mainDir <- "~/Dropbox/FEUP/FEUP_13.14/Dissertacao/Olho-Passarinho/modelo1/R_Project_server"  
  subDir <- toString(subset)
  setwd(file.path(mainDir, subDir))
  #sample <- readRDS("sample.rds")
  
  
  x <- paste("~/Dropbox/FEUP/FEUP_13.14/Dissertacao/Olho-Passarinho/modelo1/R_Project_server", subDir, sep="")
  mainDir <- x
  subDir <- "combined_matrices"
  setwd(file.path(mainDir, subDir))
  
  for(i in 1:dim(vars)[1])
  {
    x <- c("combined_matrix_", vars[i,1], "_", vars[i,2], "_",vars[i,3], "_",vars[i,4], ".rds")
    m_name <- str_replace_all(toString(x), ", ", "") 
    conbined_matrix <- readRDS(m_name)
    eps <- max(conbined_matrix)*0.1
    clustering <- dbscan(conbined_matrix, eps, MinPts=2, method = "dist")
    
    x <- c("clustering_", vars[i,1], "_", vars[i,2], "_",vars[i,3], "_",vars[i,4], ".rds")
    c_name <- str_replace_all(toString(x), ", ", "") 
    saveRDS(clustering, c_name)
    
    cat(sprintf("Detected %s new clusters\n", max(as.array(unlist(clustering$cluster)))))
    
    for(k in 1:max(as.array(unlist(clustering$cluster))))
    {
      cat(sprintf("Cluster %s has %s elements\n", k, 
                  dim(as.array(unlist(which(clustering$cluster==k))))))
    }
  }
}

calculate_clustering_dbscan2<- function(subset) 
{  
  mainDir <- "/mnt/sdb1/tweeprofiles/R_Project_server"  
  subDir <- toString(subset)
  setwd(file.path(mainDir, subDir))
  
  sp_matrix <- readRDS("sample_sp_dist_norm.rds")
  tp_matrix <- readRDS("sample_tp_dist_norm.rds")
  ct_matrix <- readRDS("sample_ct_dist_norm.rds")
  
  x <- paste("/mnt/sdb1/tweeprofiles/R_Project_server/", subDir, sep="")
  mainDir <- x
  subDir <- "combined_matrices"
  setwd(file.path(mainDir, subDir))
  
  eps <- max(sp_matrix)*0.1
  clustering <- dbscan(sp_matrix, eps, 2, method = "dist")  
  c_name <- c("clustering_1_0_0_0.rds")   
  saveRDS(clustering, c_name)
  
  cat(sprintf("Detected %s new clusters\n", max(as.array(unlist(clustering$cluster)))))
  
  for(k in 1:max(as.array(unlist(clustering$cluster))))
  {
    cat(sprintf("Cluster %s has %s elements\n", k, 
                dim(as.array(unlist(which(clustering$cluster==k))))))
  }
  rm(sp_matrix)
  
  eps <- max(tp_matrix)*0.1
  clustering <- dbscan(tp_matrix, eps, 2, method = "dist")  
  c_name <- c("clustering_0_1_0_0.rds")   
  saveRDS(clustering, c_name)
  
  cat(sprintf("Detected %s new clusters\n", max(as.array(unlist(clustering$cluster)))))
  
  for(k in 1:max(as.array(unlist(clustering$cluster))))
  {
    cat(sprintf("Cluster %s has %s elements\n", k, 
                dim(as.array(unlist(which(clustering$cluster==k))))))
  }
  rm(tp_matrix)
  
  eps <- max(ct_matrix)*0.1
  clustering <- dbscan(ct_matrix, eps, 2, method = "dist")  
  c_name <- c("clustering_0_0_1_0.rds")   
  saveRDS(clustering, c_name)
  
  cat(sprintf("Detected %s new clusters\n", max(as.array(unlist(clustering$cluster)))))
  
  for(k in 1:max(as.array(unlist(clustering$cluster))))
  {
    cat(sprintf("Cluster %s has %s elements\n", k, 
                dim(as.array(unlist(which(clustering$cluster==k))))))
  }
  rm(ct_matrix)
}


subset <- 65000
inc <- 7500
while(subset + inc <= 120000){  
  calculate_clustering_dbscan(subset) 
  #calculate_clustering_dbscan2(subset)  
  subset <- subset  + inc/2
}


# Visualize clusters as text
arr <- as.array(unlist(clustering))
for(j in 1:max(arr)){
  print(j)
  for(i in 1:dim(sample)){
    if(arr[i]== j){
      
      cat(sprintf("#\"%s\" value=\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n", 
                  sample[i,1],sample[i,3], sample[i,4],
                  sample[i,5], sample[i,6], sample[i,7]))
    }
  }
}
rm(i,j)
