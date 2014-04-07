

sp <- readRDS("/mnt/sdb1/tweeprofiles/R_Project_server/0/sample_sp_dist.rds")
tp <- readRDS("/mnt/sdb1/tweeprofiles/R_Project_server/0/sample_tp_dist.rds")
ct <- readRDS("/mnt/sdb1/tweeprofiles/R_Project_server/0/sample_ct_dist.rds")
so <- readRDS("/mnt/sdb1/tweeprofiles/R_Project_server/0/sample_so_dist_corrected.rds")

truehist(sp)
truehist(tp)
truehist(ct)

#------------------------------------------

maxs <- c(max(sp),max(tp), max(ct), max(so))
max_val <- max(maxs)

for(i in 1:dim(as.array(maxs))){
  if(i==1 && max(sp)!= max_val){
    coef <- max_val / max(sp)
    sp_n <- update_matrix(sp,coef)
  }
  else if(i==2 && max(tp)!= max_val){
    coef <- max_val / max(tp)
    tp_n <- update_matrix(tp,coef)
  }
  else if(i==3 && max(ct)!= max_val){
    coef <- max_val / max(ct)
    ct_n <- update_matrix(ct,coef)
  }
  else if(i==4 && max(so)!= max_val){
    coef <- max_val / max(so)
    so_n <- update_matrix(so,coef)
  }
}

m <- readRDS("/mnt/sdb1/tweeprofiles/R_Project_server/0/sample_so_dist_norm.rds")

#truehist(sp_n)
#truehist(tp_n)
#truehist(ct_n)

update_matrix <- function(matrix,coef){
  temp <- matrix(0,dim(matrix)[1], dim(matrix)[2])
  for(i in 1:dim(matrix)[1]){
    for(j in 1: dim(matrix)[2]){
      temp[i,j] <- matrix[i,j] * coef
    }
  }
  return(temp)
}

#----------------------------------------------

combined_matrix2 <- function(w1,w2,w3, w4,sp,tp,ct,so){
  combined_matrix <- matrix(0,dim(sp)[1],dim(sp)[1])
  
  for(i in 1:dim(combined_matrix)[1]){
    for(j in 1:dim(combined_matrix)[1]){
      combined_matrix[i,j] =   w1 * sp[i,j] + w2 * tp[i,j] + w3 * ct[i,j] + w4 * so[i,j]
    }
  }
  rm(i,j)
  return(combined_matrix)
}


comb1 <- combined_matrix2(0.25,0.25,0.25,0.25, sp_n,tp,ct_n,so_n)
comb2 <- combined_matrix2(0.25,0,0.75, sp_n,tp,ct_n)
comb3 <- readRDS("/mnt/sdb1/tweeprofiles/R_Project_server/0/combined_matrices/combined_matrix_0.25_0_0.75_0.rds")

final_cl <- dbscan(comb3, 0.1*max_val, MinPts = 2, method = "dist")
pt <- readRDS("/mnt/sdb1/tweeprofiles/R_Project_server/0/sample.rds")
plot(x=final_cl, data=pt[,5:6]) 

arr <- as.array(final_cl$cluster)
for(j in 1:max(arr)){
  print(j)
  for(i in 1:dim(arr)){
    if(arr[i]== j){
      k <- i
      cat(sprintf("#\"%s\" value=\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n", 
                  pt[k,1],pt[k,3], pt[k,4],
                  pt[k,5], pt[k,6], pt[k,7]))
    }
  }
}
rm(i,j)

clustering <- readRDS("/mnt/sdb1/tweeprofiles/R_Project_server/0/combined_matrices/clustering_0.25_0_0.75_0.rds")
plot(x=clustering, data=pt[,5:6]) 


