library(stringr)
library(network)
library(igraph)

#Create network graph
adj_matrix_followers <- readRDS("/mnt/sdb1/tweeprofiles/R_Project_server/adj_matrix_followers2.rds")
g <- graph.adjacency(adj_matrix_followers, mode = "directed")
geo_m <- readRDS("/mnt/sdb1/tweeprofiles/R_Project_server/geo_m.rds")



<#create files
create_clustering_graph_files<- function(subset){  
  
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
      
    
    arr <- as.array(unlist(cl$cluster))
    for(j in 1:max(arr)){
      cat(sprintf("cluster: %s\n",j))
      
      z <- c("cluster_graph_data", subset, "-", vars[l,1], "_", vars[l,2], "_",vars[l,3], "_",vars[l,4], "_",j, ".json")
      fname <- str_replace_all(toString(z), ", ", "")
      cat(sprintf("{\n\"nodes\": [\n"), file=fname, append=TRUE)
      
      filtered_m <- matrix(0, dim(sample)[1], dim(sample)[2])
      k <- 1
      
      
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
      
      #output data      
      users <- filtered_m[,3] #all users in cluster
      filt_users <- as.array(unique(users)) #remove repeated 
      
      cat(sprintf("# users: %s\n", dim(filt_users)))
      
      if(dim(filt_users)>1)
      {

        vec_temp <- rep(NA,dim(filt_users))
        
        s <- 1
        for(n in 1:dim(filt_users)){
          if(filt_users[n] %in% V(g)$name )
          {
            vec_temp[s] <- filt_users[n]
            s <- s + 1
          }
        }
              
        vec_temp <- vec_temp[-s: -dim(as.array(vec_temp))]
        filt_users <- as.array(vec_temp)
        
        #filter top 10 most important users (highest degree)
        if(dim(filt_users) > 10)
        {        
          elems <- sort(degree(g,v=filt_users), decreasing = T)
          filt_users <- as.array(elems[1:10])
          cat(sprintf("filtragem de utilizadores\n"))
        }
        else
        {
          elems <- sort(degree(g,v=filt_users), decreasing = T)
          filt_users <- as.array(elems[1:dim(filt_users)])
        }
        
        cat(sprintf("users:\n"))
        print(filt_users)
        
        temp <- dim(filt_users)
        
        for(p in 1:dim(filt_users)){
          if(p==temp)
          {   
            cat(sprintf("{\"name\":\"%s\"}\n", names(filt_users[p])),
                file=fname, append=TRUE)  
          }
          else
          {
            cat(sprintf("{\"name\":\"%s\"},\n", names(filt_users[p])),
                file=fname, append=TRUE) 
          }
        }
        
        cat(sprintf("],\n", filt_users[p]),file=fname, append=TRUE)      
        cat(sprintf("\"links\":[\n"), file=fname, append=TRUE)
        
        adj_mat <- matrix(0,dim(filt_users),dim(filt_users))
        
        for(p in 1:dim(filt_users)){
          for(q in 1:dim(filt_users)){
            if(p < q){  #filter unecessary calculations on adjacency matrix            
              
              source_n <- names(filt_users[p])
              dest_n <- names(filt_users[q])
              val1 <- shortest.paths(g, v=source_n, to=dest_n, mode = "in", weights = NULL,
                                     algorithm = "dijkstra")
              val2 <- shortest.paths(g, v=dest_n, to=source_n, mode = "in", weights = NULL,
                                     algorithm = "dijkstra")
              adj_mat[p,q] <- val1              
              adj_mat[q,p] <- val2                
            }
          }
        }
        
        #print(adj_mat)
        g1 <- graph.adjacency(adj_mat)
        mst <- minimum.spanning.tree(g1) 
        print(E(mst))
        print(dim(as.array(E(mst))))
        
        if(dim(as.array(E(mst)))>0) #if mst has edges
        {               
          for(s in 1:dim(as.array(E(mst))))
          {
            e1 <- get.edge(mst,s)
            source_val <- e1[1]
            dest_val <- e1[2]
            weight <- min(adj_mat[source_val,dest_val],adj_mat[dest_val,source_val])
            
            cat(sprintf("source: %s dest: %s val: %s\n",source_val-1,dest_val-1,weight))
            
            if(weight != Inf)
            {
              if(s==dim(as.array(E(mst))))
              {   
                cat(sprintf("{\"source\":%s,\"target\":%s,\"value\":%s}\n", 
                            source_val-1,dest_val-1,weight),
                    file=fname, append=TRUE)  
              }
              else
              {
                cat(sprintf("{\"source\":%s,\"target\":%s,\"value\":%s},\n", 
                            source_val-1,dest_val-1,weight),
                    file=fname, append=TRUE) 
              }
            }
          }
        }
        
       cat(sprintf("]\n}"), file=fname, append=TRUE)
        
      }
      else #single user found in clustering
      {
        cat(sprintf("single user saved: %s\n",filt_users))
        cat(sprintf("{\"name\":\"%s\"}\n", filt_users),
            file=fname, append=TRUE) 
        cat(sprintf("],\n", filt_users[p]),file=fname, append=TRUE)      
        cat(sprintf("\"links\":[\n"), file=fname, append=TRUE)
        cat(sprintf("]\n}"), file=fname, append=TRUE)
      }
            
      filtered_m <- as.data.frame(matrix(0,dim(sample)[1], dim(sample)[2])) #clean matrix
      k <- 1
      cat(sprintf("\n"))
    }
    
    rm(i,j)
  }
}

subset <- 65000 
inc <- 7500
while(subset + inc <= dim+1){  
  create_clustering_graph_files(subset)  
  subset <- subset  + inc/2
}











