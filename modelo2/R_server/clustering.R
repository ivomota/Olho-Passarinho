library('fpc')
setwd("~/Dropbox/FEUP/FEUP_13.14/Dissertacao/Olho-Passarinho/modelo2/R_server")
set.seed(665544)
x <- readRDS('../matrix_dist_norm/sample0_im_dist_norm.rds')

# mean = mean(x)
# std = sd(c(x))
# l = length(x)
# row = nrow(x)
# col = ncol(x)
# desv = (mean + (4*std))

# new_x = matrix(data = NA, nrow = row, ncol = col, dimnames = NULL)

# for (i in 1:row) {
#   for (j in 1:col){
#     n <- x[i, j]
#     if(n > desv) { x[i,j] <- 0.0 }
#   } 
# }

eps <- max(x)*0.02
ds <- dbscan(x, eps, MinPts=2, method = "dist", showplot=1)

maxim = max(ds$cluster)
len = length(ds$cluster)
j = 0
for (i in 0:maxim) {
  nam <- paste("A", i, sep = "")
  assign(nam, which(ds$cluster %in% i) )
  nam <- paste("A", i, sep = "")
  write(which(ds$cluster %in% i), file=nam, ncolumns = len)
}

