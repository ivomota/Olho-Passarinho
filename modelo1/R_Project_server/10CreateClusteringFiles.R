

#create files
create_data_files<- function(subset)
{  
  
  mainDir <- "/mnt/sdb1/tweeprofiles/R_Project_server"  
  subDir <- toString(subset)
  setwd(file.path(mainDir, subDir))
  
  sample <- readRDS("sample.rds")
  
  for(i in 1:dim(vars)[1])
  {
    x <- paste("/mnt/sdb1/tweeprofiles/R_Project_server/", subset, sep="")
    mainDir <- x
    subDir <- "combined_matrices"
    setwd(file.path(mainDir, subDir))
    
    x <- c("clustering_", vars[i,1], "_", vars[i,2], "_",vars[i,3], "_",vars[i,4], ".rds")
    m_name <- str_replace_all(toString(x), ", ", "") 
    print(m_name)
    clustering <- readRDS(m_name)
    
    mainDir <- "/mnt/sdb1/tweeprofiles/R_Project_server"  
    subDir <- "data"
    dir.create(file.path(mainDir, subDir), showWarnings = FALSE)
    setwd(file.path(mainDir, subDir))
    
    z <- c("geodata", subset, "-", vars[i,1], "_", vars[i,2], "_",vars[i,3], "_",vars[i,4], ".json")
    fname <- str_replace_all(toString(z), ", ", "") 
    print(fname)
    
    cat("{", file=fname)
    end <- dim(sample)[1] - 1
    for( i in 1:end){
      
      #y <- str_replace_all(sample[i,7], "[^[:alnum:]]", " ")  #OK
      y <- gsub("[^@#a-zA-Z0-9 ://.:?!'áéíóúàãõçÁÉÍÓÚÀÃÕÇ]","",sample[i,7])
      
      cat(sprintf("\"%s\":[%s,\"%s\", \"%s\", %s, %s, \"%s\", %s],\n", 
                  sample[i,1], sample[i,2], sample[i,3],sample[i,4],
                  sample[i,5], sample[i,6], y, clustering$cluster[i]), file=fname, append=TRUE)
    }
    y <- gsub("[^@#a-zA-Z0-9 ://.:?!'áéíóúàãõçÁÉÍÓÚÀÃÕÇ]","",sample[i,7])
    cat(sprintf("\"%s\":[%s,\"%s\", \"%s\", %s, %s, \"%s\", %s]\n", 
                sample[end,1], sample[end,2], sample[end,3],sample[end,4],
                sample[end,5], sample[end,6], y, clustering$cluster[i]), file=fname, append=TRUE)
    cat("\n}", file=fname, append=TRUE) 
  }
  
  rm(sample)
}

subset <- 65000
inc <- 7500
while(subset + inc <= 120000){  
  create_data_files(subset)  
  subset <- subset  + inc/2
}

text <- "http://www.facebook.com"
gsub("[^@#a-zA-Z0-9 ://.:?!'áéíóúàãõçÁÉÍÓÚÀÃÕÇ]","",text)
  
