# -*- coding: utf-8 -*-
'''
Created on 2015.07.01

@author: Haar_Mao
'''
import log
import cv2
import numpy as np
global HEIGHT #y,rows归一化后图片的规格，可修改
global WIDTH  #x,cols
HEIGHT = 90
WIDTH = 60

#若轮廓数大于1则将其合并
def GetFinalContour(contour,num):
    C = np.array([[[]]])
    x = 1
    for x in contour:
        C = np.concatenate((contour[0],x),axis=0)#将两个数组加到一起
    contour[0] = C
    return contour[0]

#读取图片
def ReadImg(img):
    #img = cv2.imread(filename)
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(img_gray,100,255,0)
    return thresh

#求质心
def GetMeans(thresh):
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    ContourNum = len(contours)
    if(ContourNum>1):
        cnt = GetFinalContour(contours,ContourNum)
    else:
        cnt = contours[0]
    
    M = cv2.moments(cnt)
    #求质心
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return cx,cy,cnt

#求头部质心
def GetHeadMeans(imgH): 
    
    imgT= imgH
    img1,contours,hierarchy = cv2.findContours(imgH,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    ContourNum = len(contours)
    if(ContourNum>1):
        cnt = GetFinalContour(contours,ContourNum)
    else:
        cnt = contours[0]
        
    #求取最高点和最低点
    topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
    bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])        
    log.message("Topmost=%d bottommost=%d", topmost[1],bottommost[1])
    
    height1,width1=imgT.shape[:2]  
    Nheight = height1*0.12  #头为整个身长的10%左右
    thresh = imgT[topmost[1]:int(topmost[1]+Nheight), 1:width1]
    #cv2.imshow("Head",imgT)    
    #cv2.waitKey(1000)     

    img1,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    ContourNum = len(contours)
    if(ContourNum>1):
        cnt1 = GetFinalContour(contours,ContourNum)
    else:
        cnt1 = contours[0]
        
    M1 = cv2.moments(cnt1)
    M = cv2.moments(cnt)
        
    ##求质心
    cx = int(M1['m10']/M1['m00'])
    cy = int(M['m01']/M['m00'])    
    
    
    return cx,cy,cnt


#此处的x表示cols即320,y表示rows即240
def GetNormalPic(imgm):
    global HEIGHT
    global WIDTH 
    img = ReadImg(imgm)
    #img1 = cv2.imread(filename)#重新读入图片不然后面移动时会出问题
    img1=imgm.copy()
    A = img.shape #320*240图片 rows=240 cols=320
    rows = A[0]
    cols = A[1]
    Cx,Cy,cnt = GetHeadMeans(img)  #GetMeans(img)#质心cx=278(cols) cy=127(rows)
    #求取最高点和最低点
    topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
    bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
    #人的身高(detrows)
    Height = bottommost[1] - topmost[1]
    New_X = Cx - Height*(float(1))/3 #剪切开始的坐标x
    NewWidth = Height*float(2.0)/3 #剪切的人的宽度
    M = np.float32([[1,0,0],[0,1,0]])#初始化需要移动的矩阵
    if(New_X+NewWidth>cols):#需要左移
        delt_X = cols-(New_X + NewWidth)
        M[0][2] = float(delt_X)
        dst = cv2.warpAffine(img1,M,(cols,rows))
        Person = dst[topmost[1]:bottommost[1],(New_X+delt_X):cols]#y,x 需要剪切的人的范围
    elif(New_X<0):#需要右移
        M[0][2] = float(abs(New_X))
        dst = cv2.warpAffine(img1,M,(cols,rows))
        Person = dst[topmost[1]:bottommost[1],0:NewWidth]
    else:#不需要移动
        dst = img1
        Person = dst[topmost[1]:bottommost[1],int(New_X):int(New_X+NewWidth)]
    res = cv2.resize(Person,(WIDTH,HEIGHT))
    
    #CxNew,CyNew,cntNew = GetHeadMeans(res)  #GetMeans(img)#质心cx=278(cols) cy=127(rows)
    
    return res
#调用该函数传入图片地址和最后存储图片地址即可得到归一化后的图
def Normalize(im):
    img = GetNormalPic(im)
    return img
    #cv2.imwrite(savename,img)
'''    
if __name__ == "__main__":
    img=cv2.imread("F:/Aotu3Dpicture/2015-07-07_17.04.35.png")
    img2 = GetNormalPic(img)
    savename = "F:/Aotu3Dpicture/Norm.png"
    cv2.imwrite(savename,img2)
'''
    
    
    
    
    
