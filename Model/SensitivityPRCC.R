library(ppcor)
library(sensitivity)
library(ggplot2)
library(randomForest)
library(forcats)
library(tidyverse)


Data <- read.csv("SensitivityOut04-23.csv", stringsAsFactors = TRUE)


Data_x<-Data[-c(1,51,52)]
PCC1<-pcc(X = Data_x, y=Data$TotalCFUFP, rank =TRUE, conf = 0.8, nboot = 1000)
plot(PCC1)



pairs(Data)

#8 Visuals , remaing the columns to that no error in ggplot
names(PCC1$PRCC)=c("original", "bias" ,"std.error", "minci","maxci")

#Ggplot, here is similar to a tornado plot. Also there are error bars on the 95th percentile
Sens_DF<-PCC1$PRCC 
Sens_DF$Cateogry
  
Cateogries<-c(
  "Contamination Scen",# "InitialCont" ,
  "Contamination Scen",#"ClusterSize",
  "Time",#Time_CE_H",
  "Reduction",#"Total_CE_H_Dieoff",
  
  #Pre-cooling
  "Time",#"Time_H_PC",
  "Temperature",#"Temp_H_PC",
  "Time",#"Time Precooling",
  "Time",#"Temp Precooling",
  "Intervention",#"Pre_cooling",
  #Receiving
  "Time",#"Time_Storage_R",
  "Temperature",#"Temp_Storage_R",
  #Processing Factor
  "Reduction",#"PreWashRed",
  "Reduction",#"PreWashYN",
  "Reduction",#"WashingYN",
  "Reduction", #OptimizedYN
  "Reduction", #"ChSpray_eff"
  "Processing",#"Tr_Sh_P",
  "Processing",#"Tr_P_Sh",
  "Reduction",#"Sh_Compliance",
  "Reduction",#"Sh_San_freq",
  "Reduction",#"Sh_San_Eff",
  "Processing",#"Tr_Cv_P",
  "Processing",#"Tr_P_Cv",
  "Reduction",#"Cv_Compliance",
  "Reduction",#"Cv_San_freq",
  "Reduction",#"Cv_San_Eff",
  "Processing",#"Tr_St_P",
  "Processing",#"Tr_P_St",
  "Reduction",#"St_Compliance",
  "Reduction",#"St_San_freq",
  "Reduction",#"St_San_Eff",
  "Processing",#"Tr_C_P",
  "Processing",#"Tr_P_C",
  "Reduction",#"C_Compliance",
  "Reduction",#"C_San_freq",
  "Reduction",# "C_San_Eff",
  "Time",
  "Temperature",
  "Time",
  "Temperature",
  "Time",
  "Temperature", 
  
  "Sampling",
  "Sampling",
  "Sampling",
  "Sampling",
  "Sampling",
  "Sampling",
  "Sampling"
  
)


Column_Names<-c(
  "Initial Contamination",# "InitialCont" ,
  "Cluster Size",#"ClusterSize",
  "Time CE-H",#Time_CE_H",
  "Total Pre-Harvest Die-off",#"Total_CE_H_Dieoff",
  
  #Pre-cooling
  "Time H-Pre-cooling",#"Time_H_PC",
  "Temperature H-Pre-cooling",#"Temp_H_PC",
  "Length Pre-cooling",#"Time Precooling",
  "Teperature Pre-cooling",#"Temp Precooling",
  "Pre-cooling ON",#"Pre_cooling",
  #Receiving
  "Time Storage- Receiving",#"Time_Storage_R",
  "Storage Temperature",#"Temp_Storage_R",
  #Processing Factor
  "Pre-Wash Reduction",#"PreWashRed",
  "Pre-Wash ON",#"PreWashYN",
  "Chlorinated Wash ON",#"WashingYN",
  "Optimized Washing ON",
  "Pre-Wash Efficacy", #"ChSpray_eff"
  "Tr_Sh_P",
  "Tr_P_Sh",
  "Sh_Compliance",
  "Sh_San_freq",
  "Sh_San_Eff",
  "Tr_Cv_P",
  "Tr_P_Cv",
  "Cv_Compliance",
  "Cv_San_freq",
  "Cv_San_Eff",
  "Tr_St_P",
  "Tr_P_St",
  "St_Compliance",
  "St_San_freq",
  "St_San_Eff",
 "Tr_C_P",
  "Tr_P_C",
  "C_Compliance",
  "C_San_freq",
  "C_San_Eff",
  "Time Post Processing Storage",
  "Temperature Post P Storage",
  "Time Transportation to C",
  "Temperature Transportation to C",
  "Time Consumer Storage",
  "Temperature Consumer Storage",
 "PHS 4 days ON",
 "PHS 4 Hours ON",
 "PHS 4 Intense ON",
 "Harvest S ON",
 "Receiving S ON",
 "Finished Product S ON",
 "Consumer S ON"
 
  
)
  
Sens_DF$Cateogry <-Cateogries 
rownames(Sens_DF)<-Column_Names

Sens_DF_T25<-Sens_DF %>% 
  arrange(desc(abs(original))) %>% 
  head(n=25)
dev.off()

ggplot(data = Sens_DF, aes(x=fct_reorder(rownames(Sens_DF), abs(original)),y=original , fill = Cateogry))+
  geom_bar(stat = "identity", position = "identity")+
  geom_errorbar(aes(ymin=minci, ymax=maxci), width=.1,col="blue")+
  ylab("Partial Correlation Coefficient")+
  xlab("Model Input")+
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



Data8<-Data

Data8<-replace(Data8[,],Data8[,] < 0, 0)




#Anova 


######likelyhood displacement

DFData2<-as.data.frame(cbind(Data$TotalCFUFP, Data_x))

Model<-lm(`Data$TotalCFUFP`~. , data = DFData2)
summary(Model)
RFData$WashingYN

ggplot(data= DFData2, aes(x =`Data$TotalCFUFP`, y = OptimizeWashingYN  ))+
  geom_point()

ggplot(data= DFData2, aes(x =`Data$TotalCFUFP`, y = WashingYN ))+
  geom_point()

Anova_mod<-aov(Model)

Table_Summ_An<-summary(Anova_mod)[[1]]


Vect<-predict(Model)

DFData2<-as.data.frame(cbind(Data$TotalCFUFP, Vect))

DFData3<-DFData2 %>% 
  mutate(error = Data$TotalCFUFP-Vect)


ggplot(data= DFData3, aes(Data$TotalCFUFP, Vect))+
  geom_point()


#Test training Split

## 75% of the sample size
smp_size <- floor(0.75 * nrow(RFData))

## set the seed to make your partition reproducible
set.seed(123)
train_ind <- sample(seq_len(nrow(RFData)), size = smp_size)

train <-RFData[train_ind, ]
test <- RFData[-train_ind, ]


Model<-lm(`Data$TotalCFUFP`~., data = train)
summary(Model)


Vector2<-predict(Model, newdata = test)

DFData2<-as.data.frame(cbind(test$`Data$TotalCFUFP`, Vector2))

DFData3<-DFData2 %>% 
  mutate(error =V1 -Vector2)

ggplot(data= DFData3, aes(V1, Vector2))+
  geom_point()

###Using PPcor

library(ppcor
        
