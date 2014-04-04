library(tm)
library(lsa)

calculate_content_distance <- function(init,end) {
  sample <- data_matrix[init:end,]    
  #sample_ct_dist <- matrix(0,dim(sample)[1],dim(sample)[1]) 
  mainDir <- "/mnt/sdb1/tweeprofiles/R_Project_server"  
  subDir <- toString(init - 1)
  
  #Content Matrix Normalized
  
  c <- Corpus(VectorSource(as.array(sample[,7])))
  tdm <- TermDocumentMatrix(c, control = list(weighting =function(x) weightTfIdf(x, normalize = TRUE)))
  sample_ct_dist <-  as.matrix(dissimilarity(x=tdm, method = "cosine"))
  rm(c,tdm)
  
  setwd(file.path(mainDir, subDir))
  saveRDS(sample_ct_dist, file = "sample_ct_dist.rds")
  
  rm(sample_ct_dist)
}

# Create matrices for overlapped subsets
init <- 1
inc <- 7500
while(init + inc <= dim+1){  
  end <- init + inc - 1
  calculate_content_distances(init,end)
  init <- init  + inc/2
}

