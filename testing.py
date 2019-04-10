#!/usr/bin/python3.6
import re
import os
import numpy as np
#import matplotlib.pyplot as plt
import hashlib
import base64
from diffraction_image_module import ImageD, SeriesD, ToolsD
from cryio.cbfimage import CbfImage
import matplotlib.pyplot as plt

filePath = '/media/jake/Back Up Drive/PhD/Data/Beam_Time/ESRF_BM01_November_2018/MAPbI3/MAPbI3_RLD/MAPbI3_I2/SingleCrystal/Crystal2/FullScan_290K/'
fileName = 'MAPbI3_I2_0001p_'


series= SeriesD(1,filePath,fileName)
tool = ToolsD()
tool.backgroundSubtraction(3,700,series)
"""

###############PEAKS LEFT##############################

############## Diffuse Peaks######################################
int_1 = series.sumBox(98,739,156,791)
err1 = np.sqrt(int_1)
int_2 = series.sumBox(44,898,102,951)
err2 = np.sqrt(int_2)
#Background
int_1b = series.sumBox(148,739,206,791)
err1b = np.sqrt(int_1b)
int_2b = series.sumBox(94,898,152,951)
err2b = np.sqrt(int_2b)

int_11 =(int_1/int_1b)+(int_2/int_2b)

err1 = np.sqrt(((err1/int_1)**2.0)+((err1b/int_1b)**2.0))
err2 = np.sqrt(((err1/int_1)**2.0)+((err2b/int_2b)**2.0))

err11 = np.sqrt((err1**2.0)+(err2**2.0))

int_11 = int_11/2.0
min1 = np.amin(int_11)
int_11 = (int_11-min1)
max1 = (np.amax(int_11))
int_11 = int_11/max1

err11= err11/2.0
err11= err11/max1


############## Peaks######################################
int_3 = series.sumBox(142,666,187,707)
err3 = np.sqrt(int_1)
int_4 = series.sumBox(24,985,69,1026)
err4 = np.sqrt(int_3)
#Background
int_3b = series.sumBox(192,666,237,707)
err3b = np.sqrt(int_3b)
int_4b = series.sumBox(74,985,119,1026)
err4b = np.sqrt(int_4b)

int_22=(int_3/int_3b)+(int_4/int_4b)
err3 = np.sqrt(((err3/int_3)**2.0)+((err3b/int_3b)**2.0))
err4 = np.sqrt(((err4/int_4)**2.0)+((err4b/int_4b)**2.0))

err22 = np.sqrt((err3**2.0)+(err4**2.0))

int_22= int_22/2.0
min1 = np.amin(int_22)
int_22 = (int_22-min1)
max1 = (np.amax(int_22))
int_22 = int_22/max1

err22= err22/2.0
err22= err22/max1

############################Diffuse Area######################

int_6 = series.sumBox(109,718,298,730)
err6 = np.sqrt(int_6)
int_7 = series.sumBox(76,797,165,809)
err7 = np.sqrt(int_7)
int_8 = series.sumBox(48,878,137,890)
err8 = np.sqrt(int_8)
int_9 = series.sumBox(22,965,111,977)
err9 = np.sqrt(int_9)
#Background
int_6b = series.sumBox(159,718,248,730)
err6b = np.sqrt(int_6b)
int_7b = series.sumBox(126,797,215,809)
err7b = np.sqrt(int_7b)
int_8b = series.sumBox(98,878,187,890)
err8b = np.sqrt(int_8b)
int_9b= series.sumBox(72,965,161,977)
err9b = np.sqrt(int_9b)
print(int_6,int_7,int_8,int_9)
int_44 =(int_6/int_6b)+(int_7/int_7b)+(int_8/int_8b)+(int_9/int_9b)

err6 = np.sqrt(((err6/int_6)**2.0)+((err6b/int_6b)**2.0))
err7 = np.sqrt(((err7/int_7)**2.0)+((err7b/int_7b)**2.0))
err8 = np.sqrt(((err8/int_8)**2.0)+((err8b/int_8b)**2.0))
err9 = np.sqrt(((err9/int_9)**2.0)+((err9b/int_9b)**2.0))

err44 = np.sqrt((err6**2.0)+(err7**2.0)+(err8**2.0)+(err9**2.0))

int_44 = int_44/4.0
min1 = np.amin(int_44)
int_44 = (int_44-min1)
max1 = (np.amax(int_44))
int_44 = int_44/max1

err44 = err44/4.0
err44 = err44/max1

###########################################################################





###############PEAKS RIGHT##############################

############## Diffuse Peaks######################################
int_1 = series.sumBox(1138,1324,1189,1379)
err1 = np.sqrt(int_1)
int_2 = series.sumBox(1201,1177,1252,1232)
err2 = np.sqrt(int_2)
#Background
int_1b = series.sumBox(1088,1324,1139,1379)
err1b = np.sqrt(int_1b)
int_2b = series.sumBox(1151,1177,1202,1232)
err2b = np.sqrt(int_2b)

int_11 =(int_1/int_1b)+(int_2/int_2b)

err1 = np.sqrt(((err1/int_1)**2.0)+((err1b/int_1b)**2.0))
err2 = np.sqrt(((err1/int_1)**2.0)+((err2b/int_2b)**2.0))

err11 = np.sqrt((err1**2.0)+(err2**2.0))

int_11 = int_11/2.0
min1 = np.amin(int_11)
int_11 = (int_11-min1)
max1 = (np.amax(int_11))
int_11 = int_11/max1

err11= err11/2.0
err11= err11/max1


############## Peaks######################################
int_3 = series.sumBox(1110,1393,1155,1448)
err3 = np.sqrt(int_1)
int_4 = series.sumBox(1232,1102,1277,1157)
err4 = np.sqrt(int_3)
#Background
int_3b = series.sumBox(1060,1393,1105,1448)
err3b = np.sqrt(int_3b)
int_4b = series.sumBox(1182,1102,1227,1157)
err4b = np.sqrt(int_4b)

int_22=(int_3/int_3b)+(int_4/int_4b)
err3 = np.sqrt(((err3/int_3)**2.0)+((err3b/int_3b)**2.0))
err4 = np.sqrt(((err4/int_4)**2.0)+((err4b/int_4b)**2.0))

err22 = np.sqrt((err3**2.0)+(err4**2.0))

int_22= int_22/2.0
min1 = np.amin(int_22)
int_22 = (int_22-min1)
max1 = (np.amax(int_22))
int_22 = int_22/max1

err22= err22/2.0
err22= err22/max1

############################Diffuse Area2######################

int_6 = series.sumBox(1111,1388,1186,1393)
err6 = np.sqrt(int_6)
int_7 = series.sumBox(1146,1303,1221,1308)
err7 = np.sqrt(int_7)
int_8 = series.sumBox(1173,1236,1248,1241)
err8 = np.sqrt(int_8)
int_9 = series.sumBox(1203,1166,1278,1171)
err9 = np.sqrt(int_9)
#Background
int_6b = series.sumBox(961,1388,1136,1393)
err6b = np.sqrt(int_6b)
int_7b = series.sumBox(1096,1303,1171,1308)
err7b = np.sqrt(int_7b)
int_8b = series.sumBox(1123,1236,1198,1241)
err8b = np.sqrt(int_8b)
int_9b= series.sumBox(1163,1166,1228,1171)
err9b = np.sqrt(int_9b)

int_44 =(int_6-int_6b)+(int_7-int_7b)+(int_8-int_8b)+(int_9-int_9b)

err6 = np.sqrt(((err6/int_6)**2.0)+((err6b/int_6b)**2.0))
err7 = np.sqrt(((err7/int_7)**2.0)+((err7b/int_7b)**2.0))
err8 = np.sqrt(((err8/int_8)**2.0)+((err8b/int_8b)**2.0))
err9 = np.sqrt(((err9/int_9)**2.0)+((err9b/int_9b)**2.0))

err44 = np.sqrt((err6**2.0)+(err7**2.0)+(err8**2.0)+(err9**2.0))

int_44 = int_44/4.0
min1 = np.amin(int_44)
int_44 = (int_44-min1)
max1 = (np.amax(int_44))
int_44 = int_44/max1

err44 = err44/4.0
err44 = err44/max1
###########################################################################


im,temp = np.genfromtxt('/home/jake/Documents/PhD/Data/Beam_Time/ESRF_BM01_October_2017/MAPbI3 2017_09_15/Single Crystal MAPbI3 (Same Crystal 43_53_label)/Diffuse Single Snapshot ramp down 350K to 100K and ramp up 100K to 350K/Raw_Data/data.dat',unpack=True)
int_a = series.sumBox(1187,1389,1264,1403)
#int_a = int_6 - np.amin(int_6)
#int_6 = int_6/np.amax(int_6)

plt.errorbar(temp[:240],(int_6-int_6b)[:240],yerr=(err44[:240]), c='b',markersize=3,fmt='o',capsize=2,label="Cooling")
#plt.errorbar(temp[:240],int_6[:240],yerr=(err44[:240]), c='b',markersize=3,fmt='o',capsize=2,label="Cooling")

plt.errorbar(temp[:240],int_44[:240],yerr=(err44[:240]), c='b',markersize=3,fmt='o',capsize=2,label="Cooling")
plt.errorbar(temp[240:469],int_44[240:469],yerr=(err44[240:469]),markersize=3,c='r',fmt='o',capsize=2,label="Heating")

plt.errorbar(temp[:240],int_22[:240],yerr=(err22[:240]), c='b',markersize=3,fmt='o',capsize=2,label="Cooling")
plt.errorbar(temp[240:469],int_22[240:469],yerr=(err22[240:469]),markersize=3,c='r',fmt='o',capsize=2,label="Heating")

plt.errorbar(temp[:240],int_11[:240],yerr=(err11[:240]), c='b',markersize=3,fmt='o',capsize=2,label="Cooling")
plt.errorbar(temp[240:469],int_11[240:469],yerr=(err11[240:469]),markersize=3,c='r',fmt='o',capsize=2,label="Heating")

plt.legend()
plt.xlabel("Temperature (K)")
plt.ylabel("Normalised Intensity")
plt.show()
"""