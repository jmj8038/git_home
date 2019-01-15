a <- read.csv("D:/encore/finalproject/result/merge_train_data_3_nokorean.csv")
summary(a)
length(is.na(a))
colnames(a)
nrow(a)
b <- subset(a, select=-c(1,2,9,10))
b
summary(b)

str(b)

summary(d)
b$city <-as.factor(b$city) # city factoring
class(b$city)

b$address_by_law <- as.factor(b$address_by_law) #address_by_law factoring
str(b)
b$year_of_completion <- as.factor(b$year_of_completion) #설립년도 factoring
str(b)

b$transaction_month <- substr(b$transaction_year_month,5,6) #거래년도 년, 월 분리
str(b)
b$transaction_month <-as.factor(b$transaction_month) #거래 월 factoring
nrow(b)
c <- subset(b, select=-c(2,3)) #거래 년-월. 거래일자 삭제
str(c)
summary(c)

d <- c[!is.na(c$tallest_building_in_sites), ] #층수 결측치 처리

nrow(d)

table(d$heat_fuel)
e <- d[d$heat_fuel == "gas" | d$heat_fuel == "cogeneration", ] #"-" 연료타입 결측치제거
nrow(e)

f <- e[!is.na(e$heat_fuel),] #연료타입 결측치 제거
nrow(f)
summary(f)

f$heat_type <- as.factor(f$heat_type) #난방타입 factoring
f$heat_fuel <- as.factor(f$heat_fuel) #연료타입 factoring
str(f)

table(f$front_door_structure)
g <- f[(f$front_door_structure == "corridor" | f$front_door_structure =="mixed" | f$front_door_structure == "stairway"), ]
nrow(g)
str(g)

set.seed(1)
install.packages("caret")
library("caret")
training_index <- createDataPartition(g$transaction_real_price, p=0.8, list = FALSE)
real_t <- g[training_index, ]
real_v <- g[-training_index, ]
real_model_t <- lm(transaction_real_price~., data = real_t)
summary(real_model_t)

real_pred_v <- predict(real_model_t, newdata = real_v)
real_pred_v
rmse <- sqrt(sum((real_pred_v - real_v$transaction_real_price)^2)/length(real_v$transaction_real_price))
rmse

#write. (j, file = "realestate.txt")

#차원축소
# g 활용

#install.packages("mRMRe")
##### read data #####

rawData = g #read.csv("realestatedForRegression-1.csv")

rawData
##### functions #####

kfolds = function(rawData, k){
  n = nrow(rawData)
  set.seed(123)
  randData = rawData[sample(n),]
  num = trunc(n/k)
  foldsList = list()
  for(i in 1:(k-1)){
    foldsList[[i]] = randData[(1+(i-1)*num):(i*num),]
  }
  foldsList[[k]] = randData[(1+(k-1)*num):n,]
  return(foldsList)
}

calc.r2pred = function(y, yhat){
  delta = y - yhat
  press = sum(delta^2)
  tss = sum((y-mean(y))^2)
  r2pred = 1-press/tss
  return(r2pred)
}


##### SVM-RFE #####

svmrfe = function(svm.data, numoffeatures, Type, Kernel = "radial"){
  library("e1071")
  x = svm.data[,-ncol(svm.data)]
  y = svm.data[,ncol(svm.data)]
  n = ncol(x)
  
  survivingFeaturesIndexes = seq(1:n)
  featureRankedList = vector(length=n)
  rankedFeatureIndex = n
  
  while(length(survivingFeaturesIndexes)>0){ 
    # SVM 모형 학습
    svmModel = svm(x[, survivingFeaturesIndexes], y, type=Type, kernel = Kernel)
    
    # SVM의 가중치 벡터 계산
    w = t(svmModel$coefs)%*%svmModel$SV
    
    # 가중치 벡터를 제곱하여 순서를 정하는데 사용
    rankingCriteria = w * w
    
    # 변수들의 순서를 정함
    ranking = sort(rankingCriteria, index.return = TRUE)$ix
    
    # featureRankedList를 업데이트 (가장 영향력이 부족한 변수를 낮은 순위에 저장)
    featureRankedList[rankedFeatureIndex] = survivingFeaturesIndexes[ranking[1]]
    rankedFeatureIndex = rankedFeatureIndex - 1
    
    # 가장 영향력이 부족한 변수를 제거
    (survivingFeaturesIndexes = survivingFeaturesIndexes[-ranking[1]])
  }
  
  index = sort(featureRankedList[1:numoffeatures])
  selectedData = subset(x, select = index)
  selectedData = cbind(selectedData, y)
  return(selectedData)
}

selectedData1 = svmrfe(rawData, 15, "C-classification")


##### mRMR #####

mRMR = function(rawData, numoffeatures){
  library("mRMRe")
  Data = rawData
  Data[,ncol(Data)] = as.numeric(Data[,ncol(Data)])
  dd = mRMR.data(data = Data)
  model.mRMR = mRMR.classic(data=dd, target_indices = c(ncol(Data)), feature_count = numoffeatures)
  selectedindices = as.numeric(solutions(model.mRMR)[[1]])
  selectedData = Data[,selectedindices]
  finalData = cbind(selectedData, Y = Data[,ncol(Data)])
  return(finalData)
}

selectedData2 = mRMR(rawData, 15)


##### PCA #####

pca = function(rawData){
  x = rawData[,-ncol(rawData)]
  y = rawData[,ncol(rawData)]
  pc = prcomp(x, scale = TRUE)
  
  k = 0
  R = 0
  while(R < 0.7){
    k = k + 1
    R = sum(pc[[1]][1:k])/sum(pc[[1]])
  }
  
  selectedData = cbind(pc[[5]][1:nrow(rawData), 1:k], y)
  finalData = as.data.frame(selectedData)
  return(finalData)
}

selectedData3 = pca(rawData)

##### SVM & SVR #####

svmNsvr = function(rawData, k, Kernel, Type){
  library("e1071")
  ## Kernel = "linear", "polynomial", "radial", "sigmoid"
  ## Type = "C-classification", "eps-regression"
  foldsList = kfolds(rawData, k)
  y = vector()
  yhat = vector()
  for(i in 1:k){
    trainingData = data.frame(Reduce(rbind, foldsList[-i]))
    validationData = foldsList[[i]]
    y = append(y, as.vector(as.matrix(validationData[ncol(validationData)])))
    input = trainingData[-ncol(trainingData)]
    output = trainingData[,ncol(trainingData)]
    
    model.svm = svm(input, output, kernel = Kernel, type=Type)
    pred = predict(model.svm, validationData[-ncol(validationData)])
    pred = as.numeric(as.character(pred))
    yhat = append(yhat, pred)
  }
  input = rawData[-ncol(rawData)]
  output = rawData[ncol(rawData)]
  model.svm.full = svm(input, output, kernel = Kernel, type=Type)
  pred = predict(model.svm.full, input)
  pred = as.numeric(as.character(pred))
  output = as.vector(as.matrix(output))
  
  if(Type == "C-classification"){
    accuracy.pred = 1-sum(abs(y-yhat))/length(y)
    accuracy = 1-sum(abs(output-pred))/length(output)
    return(c(accuracy, accuracy.pred))
  } else {
    r2 = 1-sum((output-pred)^2)/sum((output-mean(output))^2)
    r2pred = calc.r2pred(y, yhat)
    return(c(r2, r2pred))
  }
}


##### run code #####

result = svmNsvr(rawData, 5, "radial", "C-classification")
result.svmrfe = svmNsvr(selectedData1, 5, "radial", "C-classification")
result.mRMR = svmNsvr(selectedData2, 5, "radial", "C-classification")
result.pca = svmNsvr(selectedData3, 5, "radial", "C-classification")

