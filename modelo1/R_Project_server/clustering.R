library('fpc')

set.seed(665544)
x <- readRDS('sample_ct_dist_norm.rds')
eps <- max(x)*0.35
ds <- dbscan(x, eps, MinPts=2, method = "dist", showplot=1)

maxim = max(ds$cluster)

for (i in 0:maxim) {
  print(which(ds$cluster %in% i ))
}

#saveRDS(clustering, 'ctest')

