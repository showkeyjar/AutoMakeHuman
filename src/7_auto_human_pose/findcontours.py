# -*- coding: cp936 -*-
import cv2
import numpy as np
import log


def FindContours1(img):
    #img = cv2.imread(filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    img1,contours,hierarchy = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    #cv2.drawContours(img,contours,-1,(0,0,255),3)
   # cv2.imshow("img",img)
    #cv2.waitKey(0)
    return contours

def FindContours(OrigalIm):
    img = OrigalIm #cv2.imread(filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    img1,contours,hierarchy = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    #cv2.drawContours(img,contours,-1,(0,0,255),1)
    #cv2.imshow("img",img)
    #cv2.waitKey(1000)
    return contours

def MatchContours(contour1,contour2):
    deltContour = cv2.matchShapes(contour1,contour2,3,0)
  #  print(deltContour)
    return deltContour
    
def GetFinalContour(contour,num):
    C = np.array([[[]]])
    x=1
    if(num > 1):
        for x in contour:
            C = np.concatenate((contour[0],x),axis=0)#将两个数组加到一起
        contour[0] = C
 #   else:
#        print("only one contour！")
    return contour[0]

def CalDiff(img, img2):
    imgDiff = cv2.absdiff(img, img2)
    cv2.imshow("imgDiff",imgDiff)
    cv2.waitKey(1000) 
    height1,width1=img.shape[:2]    
    Normal = 255*height1*width1    
    Sum=imgDiff.sum()
    Sum=Sum+0.001
    AVR=Sum/Normal    
    log.message("height= %d width=%d Normal=%f AVR=%f", height1,width1,Normal,AVR)
    return AVR


def GetDeltValue(img,img2):
    contour1 = FindContours1(img)
    contour2 = FindContours(img2)
    
    #cv2.drawContours(img,contour1,-1,(0,0,255),1)
    #cv2.imshow("img1",img)
    #cv2.waitKey(1000)    
    
    #cv2.drawContours(filename2,contour2,-1,(0,0,255),1)
    #cv2.imshow("img2",filename2)
    #cv2.waitKey(1000)    
    num1 = len(contour1)
    num2 = len(contour2)
  #  print(num1)
  #  print(num2)
    C1 = GetFinalContour(contour1,num1)
    C2 = GetFinalContour(contour2,num2)
    
    cv2.drawContours(img,C1,-1,(0,0,255),1)
    cv2.imshow("img1",img)
    #cv2.waitKey(1000)    
    
    cv2.drawContours(img2,C2,-1,(0,0,255),1)
    cv2.imshow("img2",img2)
    cv2.waitKey(1000)        
    
    #print(len(C1))
    #print(len(C2))
    deltV = MatchContours(C1,C2)
    return deltV

#主函数，调用该函数传入两张图片地址即可得到轮廓差值
#def MainMatch(filename1,filename2):
#    delt = GetDeltValue(filename1,filename2)
   # print(delt)

'''
if __name__ == '__main__':
    filename1 = "C://Users//Administrator//Desktop//pic//23-81.png"
    filename2 = "C://Users//Administrator//Desktop//pic//23-68.png"
    delt = GetDeltValue(filename1,filename2)
    print(delt)
'''    

        
            
        
