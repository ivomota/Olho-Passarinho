library('fpc')

set.seed(665544)
x <- readRDS('R_Project_server/sample_ct_dist_norm.rds')
eps <- max(x)*0.15
ds <- dbscan(x, eps, MinPts=2, method = "dist", showplot=1)

# maxim = max(ds$cluster)
len = length(ds$cluster)


#vetor <- vetor()  # initialize

# for (i in 0:maxim) {
#   print(which(ds$cluster %in% i ))
# }

write(ds$cluster, file='ctest.txt', ncolumns = len)

