library("stringr")

create_cluster_time_data_files <- function(subset){
  
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
    
    z <- c("clustertimedata", subset, "-", vars[l,1], "_", vars[l,2], "_",vars[l,3], "_",vars[l,4], ".json")
    fname <- str_replace_all(toString(z), ", ", "")
    med_t <- min(sample[,4])
    cat(sprintf("init timestamp: %s\n",med_t))
    cat(sprintf("[\n
                {\n"), file=fname, append=TRUE)
    cat(sprintf("\"id\": \"ClusteringTimeline\",\n
                \"title\": \"\",\n
                \"focus_date\":\"%s\",\n
                \"initial_zoom\": \"10\",\n
                \"color\": \"#825000\",\n
                \"size_importance\": \"true\",\n
                \"events\":\n
                [\n", med_t), file=fname, append=TRUE)
    
    filtered_m <- matrix(0, dim(sample)[1], dim(sample)[2])
    k <- 1
    
    arr <- as.array(unlist(cl$cluster))
    for(j in 1:max(arr)){
      cat(sprintf("cluster: %s\n",j))
      for(i in 1:dim(sample)[1]){
        if(arr[i]== j){
          
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
      
      min_t <- min(filtered_m[,4])
      max_t <- max(filtered_m[,4])
      
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
        word <- gsub("[^@#a-zA-Z0-9 ://.:?!'áéíóúàãõçÁÉÍÓÚÀÃÕÇ]","",temp)  
        word <- str_replace_all(toString(word),", ", " ")

      }
         
      cat(sprintf("most relevant word: %s\n",word))
      
      #write data to file 
      
      cl_name <- paste("cluster",j, sep="")
      
     
      cat(sprintf("{\n
                    \"id\": \"%s\",\n
                  \"title\": \"%s\",\n
                  \"startdate\": \"%s\",\n
                  \"enddate\": \"%s\",\n
                  \"description\": \"Number of tweets: %s Most relevant words:%s\",\n",
                  j,cl_name,min_t, max_t,k, word),
          file=fname, append=TRUE)
      
      importance <- (k/dim(sample)[1])*100
      
      
      cat(sprintf("\"event_type\": \"event\",\n
                  \"icon\": \"triangle_green.png\",\n
                  \"low_threshold\": \"1\",\n
                  \"high_threshold\": \"60\",\n
                  \"importance\": \"%s\",\n
                  \"ypix\": \"0\",\n
                  \"slug\":\"\"\n
                  }\n", importance), file=fname, append=TRUE)
      
      temp <- max(arr)

      if(j!=temp){
        cat(sprintf(","), file=fname, append=TRUE)
      }
      
      
      filtered_m <- as.data.frame(matrix(0,dim(sample)[1], dim(sample)[2])) #clean matrix
      k <- 1
      cat(sprintf("\n"))
    }
    
    cat(sprintf("]\n}\n]"), file=fname, append=TRUE)
    rm(i,j)
  }
}


#calculate files for all subsets


subset <- 65000
inc <- 7500
while(subset + inc <= 120000){  
  create_cluster_time_data_files(subset)  
  subset <- subset  + inc/2
}



