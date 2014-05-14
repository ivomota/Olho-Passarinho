library(stringr)
library(tm)

create_cluster_data_files <- function(subset){
  
  mainDir <- "/mnt/sdb1/tweeprofiles/R_Project_server"  
  subDir <- toString(subset)
  setwd(file.path(mainDir, subDir))
  
  sample <- readRDS("sample.rds")
  
  
  mainDir <- "/mnt/sdb1/tweeprofiles/R_Project_server"  
  subDir <- "data"
  dir.create(file.path(mainDir, subDir), showWarnings = FALSE)
  setwd(file.path(mainDir, subDir))
  
  
  
  for(l in 1:dim(vars)[1])
  {
    x <- paste("/mnt/sdb1/tweeprofiles/R_Project_server/", subset, sep="")
    mainDir <- x
    subDir <- "combined_matrices"
    setwd(file.path(mainDir, subDir))
    
    x <- c("clustering_", vars[l,1], "_", vars[l,2], "_",vars[l,3], "_",vars[l,4], ".rds")
    m_name <- str_replace_all(toString(x), ", ", "") 
    print(m_name)
    cl <- readRDS(m_name)    
    
    mainDir <- "/mnt/sdb1/tweeprofiles/R_Project_server"  
    subDir <- "data"
    dir.create(file.path(mainDir, subDir), showWarnings = FALSE)
    setwd(file.path(mainDir, subDir))
    
    z <- c("clusterdata", subset, "-", vars[l,1], "_", vars[l,2], "_",vars[l,3], "_",vars[l,4], ".json")
    fname <- str_replace_all(toString(z), ", ", "")
    cat(sprintf("{\n"), file=fname, append=TRUE)
    cat(sprintf("\"%s\":[%s,%s,%s,\"%s\",\"%s\"],\n", 
                "cluster",0.0,0.0, 0.0,"0000-00-00 00:00", "0000-00-00 00:00"),
        file=fname, append=TRUE)    #dummy line for visualization purposes
    
    filtered_m <- matrix(0, dim(sample)[1], dim(sample)[2])
    k <- 1
    
    arr <- as.array(unlist(cl$cluster))
    for(j in 1:max(arr)){
      cat(sprintf("cluster: %s\n",j))
      for(i in 1:dim(sample)[1]){
        if(arr[i]== j){
          
          #cat(sprintf("#\"%s\" value=\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n", 
          #            sample[i,1],sample[i,3], sample[i,4],
          #            sample[i,5], sample[i,6], sample[i,7]))
          filtered_m[k,1] <- sample[i,1]
          filtered_m[k,2] <- sample[i,2]
          filtered_m[k,3] <- sample[i,3]
          filtered_m[k,4] <- sample[i,4]
          filtered_m[k,5] <- sample[i,5]
          filtered_m[k,6] <- sample[i,6]
          filtered_m[k,7] <- sample[i,7]
          
          k <- k + 1
        }
      }
      
      #remove empty lines
      dim <- dim(filtered_m)[1]      
      filtered_m <- filtered_m[-k: -dim,]
      dim = dim(filtered_m)[1]
      k <- k - 1
      
      cat(sprintf("# elements: %s\n", k))
    
      #output statistics
    
      med1 <- mean(as.numeric(filtered_m[,5]))
      med2 <- mean(as.numeric(filtered_m[,6]))
      
      lat1 <- quantile(as.numeric(filtered_m[,5]))[4]
      lat2 <- quantile(as.numeric(filtered_m[,5]))[1]
      min_lat <- min(lat1,lat2)
      max_lat <- max(lat1,lat2)
      
      lgt1 <- quantile(as.numeric(filtered_m[,6]))[4]
      lgt2 <- quantile(as.numeric(filtered_m[,6]))[1]
      min_lgt <- min(lgt1,lgt2)
      max_lgt <- max(lgt1,lgt2)  
      
      max_distance <- hf(deg2rad(as.numeric(min_lat)),
                       deg2rad(as.numeric(min_lgt)),
                       deg2rad(as.numeric(max_lat)),
                       deg2rad(as.numeric(max_lgt)))
      
      abs_radius <- max_distance / 2
      
      cat(sprintf("average radius: %s\n",abs_radius))
      cat(sprintf("average lat/lgt: %s - %s\n",med1, med2))
      
      tmp <- filtered_m[,4]
      min_t <- min(tmp)
      max_t <- max(tmp)
      
      cat(sprintf("minimum timestamp: %s\n",min_t))
      cat(sprintf("maximum timestamp: %s\n",max_t))
      
      c <- Corpus(VectorSource(as.array(filtered_m[,7])))
      tdm <- as.matrix(TermDocumentMatrix(c, control = list(weighting =function(x) weightTfIdf(x, normalize = TRUE))))
      #print(filtered_m[,7])
      ind <- which(tdm == max(tdm), arr.ind=TRUE)
      
      words <- rep("", 4)
      word <- "I"
      count <- 1
      if(dim(tdm)!=0)
      {
        for(p in 1:dim(ind)[1]){
          if(p <= 4) # maximum 4 words
          {
            val <- rownames(tdm)[ind[p]]
            if(val %in% words)
            {
              print("repeated word")
            }
            else{
              words[count] <- rownames(tdm)[ind[p]]
              count <- count + 1
            }
          }
        }           
        
        temp <- c(words[1], " ", words[2], " ", words[3], " ", words[4])
        word <- toString(temp)
      }
      #word <- str_replace_all(word, "[^[:alnum:]]", " ")  #OK
      word <- gsub("[^@#a-zA-Z0-9 ://.:?!'áéíóúàãõçÁÉÍÓÚÀÃÕÇ]","",word)
      cat(sprintf("most relevant word: %s\n",word))
               
      cl_name <- paste("cluster",j, sep="")
      
      temp <- max(arr)
      
      if(j==temp)
      {
        cat(sprintf("\"%s\":[%s,%s,%s,\"%s\",\"%s\",%s,\"%s\"]\n", 
                    cl_name,med1, med2, abs_radius, min_t, max_t, k, word),
            file=fname, append=TRUE)
      }
      else
      {
        cat(sprintf("\"%s\":[%s,%s,%s,\"%s\",\"%s\",%s,\"%s\"],\n", 
                    cl_name,med1, med2, abs_radius, min_t, max_t, k, word),
            file=fname, append=TRUE)
      }      
     
      
      filtered_m <- as.data.frame(matrix(0,dim(sample)[1], dim(sample)[2])) #clean matrix
      k <- 1
      cat(sprintf("\n"))
    }
    
    cat(sprintf("}"), file=fname, append=TRUE)
    rm(i,j)
  }
}


#calculate files for all subsets


subset <- 0
inc <- 7500
while(subset + inc <= 120000){  
  create_cluster_data_files(subset)  
  subset <- subset  + inc/2
}


