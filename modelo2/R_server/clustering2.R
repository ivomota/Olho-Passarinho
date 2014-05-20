library('fpc')
# setwd("~/Dropbox/FEUP/FEUP_13.14/Dissertacao/Olho-Passarinho/modelo2/R_server")
set.seed(665544)
x <- readRDS('../matrix_dist_norm/sample2_im_dist_norm.rds')

eps <- max(x)*0.02
ds <- dbscan(x, eps, MinPts=5, method = "dist", showplot=1)

maxim = max(ds$cluster)
len = length(ds$cluster)
j = 0
for (i in 0:maxim) {
  nam <- paste("C", i, sep = "")
  assign(nam, which(ds$cluster %in% i) )
  # nam <- paste("S2", nam, sep = "_")
  nam <- paste(nam, "txt", sep = ".")
  nam <- paste("../R_server/clusters/S2", nam, sep="/")
  write(which(ds$cluster %in% i), file=nam, ncolumns = len)
}

