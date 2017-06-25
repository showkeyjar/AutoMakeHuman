# -*- coding: utf-8 -*-
'''
Created on 2015.06.29

@author: Haar_Mao
'''
import numpy as np
import cv2
import math
global ContourNum
ContourNum = 128

#计算2点之间的距离
def Length2D(point_2,point_1):
    t1 = math.pow(float(point_2[0]-point_1[0]),2)
    t2 = math.pow(float(point_2[1]-point_1[1]),2)
    t3 = math.pow(float(t1+t2),float(0.5))
    return t3

#bilinear interpolation 双线性插值
def BilInter(point_2,point_1,length):
    ratio = length/Length2D(point_2,point_1)
    #print ratio
    x = point_2[0]+(point_1[0]-point_2[0])*ratio
    y = point_2[1]+(point_1[1]-point_2[1])*ratio
    return x,y

def GetImgContour(filename):
    img = cv2.imread(filename)
    #img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #ret,thresh = cv2.threshold(img_gray,100,255,0)
    #img,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    img,contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    '''
    cv2.drawContours(img,contours,-1,(0,0,255),3)
    cv2.imshow("img",img)
    cv2.waitKey(0)
    '''
    return contours
#得到128个轮廓点
def GetPoint(contours):
    global ContourNum
    cnt = contours[0]
    ContourLength = cv2.arcLength(cnt,True) #求轮廓周长
    Avelenth = (float(ContourLength))/ContourNum  #每份轮廓的长度
    TotalNum = len(cnt)#轮廓点的个数
    Point_1 = []#原始点数的存储
    for x in cnt:
        Point_1.append(x[0])
    Point_2 = []#所求轮廓点存储
    #初始化
    for n in range(ContourNum):
        Point_2.append(np.array([0,0]))
    Point_2[0][0] = Point_1[0][0]
    Point_2[0][1] = Point_1[0][1]
    d=len(Point_2)
    print d
    j=1
    #求取最佳轮廓点
    for i in range(ContourNum-1):
        j = int(math.fmod(j,TotalNum))
        if(float(Length2D(Point_2[i],Point_1[j])) > Avelenth):
            x,y = BilInter(Point_2[i],Point_1[j],Avelenth)

            Point_2[i+1][0] = x
            Point_2[i+1][1] = y

            i = i+1
        else:
            s1 = float(Length2D(Point_2[i],Point_1[j]))
            
            while(s1+float(Length2D(Point_1[j],Point_1[j+1]))<Avelenth):
                s6 = float(Length2D(Point_1[j],Point_1[j+1]))
                s1 = s1+s6
                j=j+1
                
            x1,y1 = BilInter(Point_1[j],Point_1[j+1],Avelenth-s1)
            Point_2[i+1][0] = int(x1)
            Point_2[i+1][1] = int(y1)

            i=i+1
            j=j+1
            
    C_Point = []
    for num1 in range(ContourNum):
        C_Point.append([0,0])
        
    for num2 in range(ContourNum):
        C_Point[num2][0] = Point_2[num2][0]
        C_Point[num2][1] = Point_2[num2][1]
    #sorted(C_Point,key = lambda x:x[1])
    #print C_Point
    return C_Point

def WriteFile(savename,Point):
    myfile = open(savename,'w')
    Length = len(Point)
    for i in range(Length):
        myfile.write(str(Point[i][0]))
        myfile.write('  ')
        myfile.write(str(Point[i][1]))
        myfile.write('\n')
    myfile.close

#主函数，调用该函数通过传递图片地址和存储点坐标的txt地址可得到轮廓点
def MainGetContourPoint(filename,savename):
    contours = GetImgContour(filename)
    Point = GetPoint(contours)
    WriteFile(savename,Point)
'''
if __name__ == '__main__':
    filename = "C://Python27//1.png"
    contours = GetImgContour(filename)
    Point = GetContourPoint(contours)
    savename = "C://Users//Administrator//Desktop//pic//lunkuo.txt"
    WriteFile(savename,Point)
'''         
            
            
            
        
    
    
        
        
    
    
    
    


