library(rmongodb)
library(stringr)

#Timestamp converter function ("2012-05-31T23:56:31Z")
to_POSIX <- function(z) {  
  x <- str_replace_all(z, "[TZ]", " ")
  return(strptime(x, "%F %X "))
}

#view data util function (includes rownames)
viewData = function(x) {
  if (!is.null(rownames(x))) {
    View(data.frame(rn=rownames(x), x))
  } else {
    View(x)
  }
}

#Read data from TwitterEcho's MongoDB
mongo <- mongo.create(host="192.168.102.195", name="",db="twitterecho")
dim <- mongo.count(mongo, "twitterecho.geotagged_tweets", query=mongo.bson.empty())
data_matrix <- matrix(0,dim,7)
colnames(data_matrix) <- c("status_id", "user_id", "user_name", "timestamp", "latitude", "longitude", "text")

if (mongo.is.connected(mongo)) {
  buf <- mongo.bson.empty() #all objects
  
  b <- mongo.find(mongo, "twitterecho.geotagged_tweets", query=buf)
  i <- 0
  if (!is.null(b)){
    while (mongo.cursor.next(b)){      
      obj <- mongo.cursor.value(b)   
      lat <- mongo.bson.value(obj, "value.coordinates.latitude")      
      lgt <- mongo.bson.value(obj, "value.coordinates.longitude")
      
      if((lat >= -90 && lat <= 90 && lgt >= -180 && lgt <= 180))  #Filter valid lat/lgt        
      {    
        
        data_matrix[i,1] <- substr(mongo.bson.value(obj, "_id"), 1, 9)
        data_matrix[i,2] <- mongo.bson.value(obj, "value.status_user_id")
        data_matrix[i,3] <- mongo.bson.value(obj, "value.status_user_name")
        data_matrix[i,4] <- toString(to_POSIX(mongo.bson.value(obj, "value.created_at")))
        
        if(i <= 84023){
        data_matrix[i,5] <- mongo.bson.value(obj, "value.coordinates.latitude")
        data_matrix[i,6] <- mongo.bson.value(obj, "value.coordinates.longitude")
        }
        else
        {
          data_matrix[i,6] <- mongo.bson.value(obj, "value.coordinates.latitude")
          data_matrix[i,5] <- mongo.bson.value(obj, "value.coordinates.longitude")
        }
        data_matrix[i,7] <- str_replace_all(mongo.bson.value(obj, "value.status_text"), "([\"])", "")
        i <- i + 1    
      }
    }
  }
}

mongo.disconnect(mongo)
rm(b,buf,i,mongo,obj,lat,lgt)

#write.table(unique(data_matrix[,3]), file = "/mnt/sdb1/tweeprofiles/R_Project_server/geo_users.csv", 
#            sep = ",", row.names=FALSE, col.names = FALSE)

#Remove empty lines in data_matrix
index <- which(data_matrix[,1] == 0)[1]
index <- index - 1
data_matrix <- data_matrix[-index: -dim,]
dim = dim(data_matrix)[1]
rm(index)

#Data timestamp distribution analysis
times <- matrix(0,2,12) 
colnames(times) <- c("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
rownames(times) <- c(2012,2013)
faults <- 0
for(i in 1:dim){
  x <- as.integer(strptime(data_matrix[i,4], "%F %X")$year + 1900)
  y <- as.integer(strptime(data_matrix[i,4], "%F %X")$mon + 1)
  
  if(is.na(x)){
    x <- as.integer(strptime(data_matrix[i,4], "%F")$year + 1900)
    y <- as.integer(strptime(data_matrix[i,4], "%F")$mon + 1)
    cat(sprintf("%s -> %s\n", x, y))
  }
  
  if(!is.na(x)){
    
    if(x == 2012){
      times[1,y] <-  times[1,y] + 1
    }
    else if(x == 2013){
      times[2,y] <-  times[2,y] + 1
    }
  }
  else{
    faults <- faults + 1
    print(i)
  }
  
}
sum(times)
viewData(times)

rm(x,y,i,faults)

#correct NA in timestamp (only one index faulty)
which(data_matrix[,4]=="NA")
data_matrix[84023,4] = "2015-01-01 00:00:00"