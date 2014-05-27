library('fpc')
library("stringr", lib.loc="/Library/Frameworks/R.framework/Versions/2.15/Resources/library")
set.seed(665544)
mainDir <- "~/Dropbox/FEUP/FEUP_13.14/Dissertacao/Olho-Passarinho/modelo2/matrix_combined/S1"
setwd(file.path(mainDir))

a <- c(1, 0.75, 0.75, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0, 0)
b <- c(0, 0.25, 0, 0.5, 0.25, 0, 0.75, 0.5, 0.25, 0, 1, 0.75, 0.5, 0.25, 0)
c <- c(0, 0, 0.25, 0, 0.25, 0.5, 0, 0.25, 0.5, 0.75, 0, 0.25, 0.5, 0.75, 1)
len <- length(a)

for (j in 1:len){
  print(j)
  
  x <- c("combined_matrix_", a[j], "_", b[j], "_", c[j], ".rds")
  m_name <- str_replace_all(toString(x), ", ", "") 
  conbined_matrix <- readRDS(m_name)
  eps <- max(conbined_matrix)*0.02
  ds <- dbscan(conbined_matrix, eps, MinPts=5, method = "dist", showplot=1)
  x <- c("c_", a[j], "_",b[j], "_",c[j])
  c_name <- str_replace_all(toString(x), ", ", "")
  dir <- paste("clusters", c_name, sep="/")
  dir.create(dir)
  maxim = max(ds$cluster)
  len = length(ds$cluster)
  for (i in 0:maxim) {
    nam <- paste("c", i, sep = "")
    assign(nam, which(ds$cluster %in% i) )
    nam <- paste(nam, "txt", sep = ".")
    way <- paste("./clusters", c_name, sep="/")
    name <- paste(way, nam, sep="/")
    write(which(ds$cluster %in% i), file=name, ncolumns = len)
  }
  #   saveRDS(ds, c_name)
  
  cat(sprintf("Detected %s new clusters\n", max(as.array(unlist(ds$cluster)))))
  
  for(k in 1:max(as.array(unlist(ds$cluster))))
  {
    cat(sprintf("Cluster %s has %s elements\n", k, 
                dim(as.array(unlist(which(ds$cluster==k))))))
  }
}

# maxim = max(ds$cluster)
# len = length(ds$cluster)
# j = 0
# 
# for (i in 0:maxim) {
#   nam <- paste("C", i, sep = "")
#   assign(nam, which(ds$cluster %in% i) )
#   nam <- paste(nam, "txt", sep = ".")
#   nam <- paste("../R_server/clusters/S0", nam, sep="/")
#   write(which(ds$cluster %in% i), file=nam, ncolumns = len)
# }