library(ppcor)
library(sensitivity)
library(ggplot2)
library(randomForest)
library(forcats)


Data <- read.csv("SensitivityOut01-27.csv", stringsAsFactors = TRUE)
Data<-Data[-c(1)]
Data<-Data[-c(12)]
Data<-Data[-c(8)]
Data_x<-Data[-c(19)]
PCC1<-pcc(X = Data_x, y=Data$TotalCFUFP, rank =TRUE, conf = 0.8, nboot = 1000)
plot(PCC1)



pairs(Data)

#8 Visuals , remaing the columns to that no error in ggplot
names(PCC1$PRCC)=c("original", "bias" ,"std.error", "minci","maxci")

#Ggplot, here is similar to a tornado plot. Also there are error bars on the 95th percentile



ggplot(data = PCC1$PRCC, aes(x=fct_reorder(rownames(PCC1$PRCC), abs(original)),y=original ))+
  geom_bar(stat = "identity", position = "identity")+
  geom_errorbar(aes(ymin=minci, ymax=maxci), width=.1,col="blue")+
  ylab("Partial Correlation Coefficient")+
  xlab("Action")+
  ggtitle("Sensitivity Analysis on Final CFU in System")+
  coord_flip()+
  theme(plot.title = element_text(hjust = 0.5))+
  theme(text = element_text(size=13))


DataLocalSampling<-read.csv("Sampling_Plan_Sens.csv", stringsAsFactors = TRUE)


DataLocalSampling<-DataLocalSampling[-c(1)]

PCCLocal<-pcc(X = DataLocalSampling[1:4], y=DataLocalSampling$PerReject, rank =TRUE, conf = 0.95, nboot = 1000)

plot(PCCLocal)

#8 Visuals , remaing the columns to that no error in ggplot
names(PCCLocal$PRCC)=c("original", "bias" ,"std.error", "minci","maxci")

#Ggplot, here is similar to a tornado plot. Also there are error bars on the 95th percentile



ggplot(data = PCCLocal$PRCC, aes(x=fct_reorder(rownames(PCCLocal$PRCC), abs(original)),y=original ))+
  geom_bar(stat = "identity", position = "identity")+
  geom_errorbar(aes(ymin=minci, ymax=maxci), width=.1,col="blue")+
  ylab("Partial Correlation Coefficient")+
  xlab("Action")+
  ggtitle("Sensitivity Analysis on Final CFU in System")+
  coord_flip()+
  theme(plot.title = element_text(hjust = 0.5))+
  theme(text = element_text(size=13))
