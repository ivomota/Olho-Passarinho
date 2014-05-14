
library(stringr)
library(network)
library(igraph)


mainDir <- "/mnt/sdb1/tweeprofiles"  
subDir <- "R_Project_server"
setwd(file.path(mainDir, subDir))
geo_users <- read.csv("geo_users.csv", sep=",")
geo_users <- as.matrix(geo_users)

#Read followers/friends input file
followers_friends_m <- as.matrix(read.csv("final_matrix.csv", sep=","))
colnames(followers_friends_m) <- c("screen_name", "followers", "friends")


#clean data frame
for(i in 1:dim(followers_friends_m)[1])
{
  val <- followers_friends_m[i,1]
  followers_friends_m[i,1] = str_replace_all(val, " ", "")
}

#Merge matrices by username
final_m <- merge(as.data.frame(geo_users), 
                 as.data.frame(followers_friends_m), 
                 by.x = "screen_name", by.y = "screen_name")
saveRDS(final_m, file = "final_m.rds")
final_m <- unique(final_m)


#create adjacency matrix
adj_matrix_followers <- matrix(0,dim(final_m)[1], dim(final_m)[1])  
colnames(adj_matrix_followers) <- final_m[,1]

for(i in 1:dim(final_m)[1]){
  user1 <- str_replace_all(as.character(final_m[i,2]), " ", "") #left
  
  s <- as.vector(final_m[i,3])
  s <- str_replace_all(s, " ", "")
  res <- unlist(strsplit(s, ":"))

  
  for(j in 1:dim(final_m)[1]){
    user2 <-  str_replace_all(as.character(final_m[j,2]), " ", "") #right

    if(!is.na(pmatch(user2,res)))
    {
      adj_matrix_followers[j,i] = 1
    }
  }
}
saveRDS(adj_matrix_followers, file="adj_matrix_followers.rds")

max(adj_matrix_followers)
which(adj_matrix_followers[1:100,1:100]==1)
adj_matrix_followers[971]

#update inverse relationship wheen missing value for follower with friend ids
for(i in 1:dim(final_m)[1]){
  user1 <- final_m[i,2] #left
  
  s <- as.vector(final_m[i,4])
  s <- str_replace_all(s, " ", "")
  res <- unlist(strsplit(s, ":"))
  
  for(j in 1:dim(final_m)[1]){
    user2 <- final_m[j,2] #right
    
    if(!is.na(pmatch(user2,res)))
    {
      adj_matrix_followers[i,j] = 1
    }
  }
}
rm(i,j,res,s,user1,user2)
saveRDS(adj_matrix_followers, file="adj_matrix_followers2.rds")

#Create networks
g <- graph.adjacency(adj_matrix_followers, mode = "directed")
g2 <- delete.vertices(g, which(degree(g) < 1))

layout <- layout.fruchterman.reingold(g2) 
plot(g2, vertex.shape="circle", vertex.label=NA, #vertex.label.cex=1, 
     vertex.size=3,edge.arrow.size=0.25, layout=layout)

#shortest path
shortest.paths(g, v="AndreCNobre", to="_marianapacheco", mode = "in", weights = NULL,
               algorithm = "dijkstra")

shortest.paths(g, v="andrefgarcia", to="__tomaz", mode = "in", weights = NULL,
               algorithm = "dijkstra")

shortest.paths(g, v="_ricardo27", to="_AnaJorge_", mode = "in", weights = NULL,
               algorithm = "dijkstra")

shortest.paths(g, v="_AnaJorge_", to="_ricardo27", mode = "in", weights = NULL,
               algorithm = "dijkstra")

shortest.paths(g, v="_FelipeLeitte", to="_GodoyP", mode = "in", weights = NULL,
               algorithm = "dijkstra")

#get path
arr1 <- get.shortest.paths(g, from="_GodoyP", to="_ricardo27", mode = "in", weights = NULL,
               output = "vpath")
final_m[unlist(arr1),1]
#[1] _GodoyP    blaine     bpedro     AnaMartelo _ricardo27
  

calculate_geo_users_socialdistance <- function(geo) {
  geo_dist <- matrix(dim,dim(geo),dim(geo))  

  for(i in 1:dim(geo)[1]){ 
    user_left <- as.character(geo[i,2])
    
    if(!is.na(match(user_left, V(g)$name)))
    {
      for(j in 1:dim(geo)[1]){
        user_right <- as.character(geo[j,2])
        
        if(!is.na(match(user_right, V(g)$name)))
        {
          dist <-shortest.paths(g, 
                                               v=user_left, 
                                               to=user_right, 
                                               mode = "in", weights = NULL,
                                               algorithm = "dijkstra")
          
          if(dist != dim)            
            geo_dist[i,j] = dist
          print(dist)
        }        
      }
    }
    print(i)
  }
  rm(i,j)
  
  saveRDS(geo_dist, file = "geo_dist.rds")
  
  return(geo_dist)
}


#match("vampaz", V(g)$name)

geo_m <- calculate_geo_users_socialdistance(geo_users)
saveRDS(geo_m, "geo_m.rds")

for(i in 1:dim(geo_m)[1]){
  for(j in 1:dim(geo_m)[2])
  {
    if(geo_m[i,j] == 119558)
      geo_m[i,j] = 9362
  }
}

saveRDS(geo_m, "geo_m_corrected.rds")
min(geo_m)
max(geo)

# Calculate all dissimilarity matrices (spatial, temporal, content) raw and normalized
# for a given subset with indexes in interval [init,end]
calculate_social_distance <- function(init,end) {
 
  
  mainDir <- "/mnt/sdb1/tweeprofiles/R_Project_server" 
  subDir <- toString(init - 1)
  setwd(file.path(mainDir, subDir))
  
  sample <- readRDS("sample.rds")
  sample_so_dist <- matrix(0,dim(sample)[1],dim(sample)[1]) 
  
  #Spatial Matrix
  for(i in 1:dim(sample)[1]){
    user1 <- sample[i,3]
    #print(user1)
    for(j in 1:dim(sample)[1]){
      user2 <- sample[j,3]
      #print(user2)
      
      ind1 <- which(geo_users[,2] == user1)
      #print(ind1)
      ind2 <- which(geo_users[,2] == user2)
      #print(ind2)
      
      sample_so_dist[i,j] = geo_m[ind1,ind2]
    }
  }
  rm(i,j)
  
  
  saveRDS(sample_so_dist, file = "sample_so_dist.rds")
  
  rm(sample_so_dist)
}

#Calculate subsets
init <- 1
inc <- 7500
while(init + inc <= dim+1){  
  end <- init + inc - 1
  calculate_social_distance(init,end)
  init <- init  + inc/2
}