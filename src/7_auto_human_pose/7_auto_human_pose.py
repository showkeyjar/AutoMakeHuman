# -*- coding: utf-8 -*-
import OpenGL
import gui
import gui3d
import mh
import cv2
import log
import animation
import bvh
import os
import getpath
import filecache
import sys
import time
import os.path
import glmodule
import numpy as np
import filechooser as fc
from core import G
OpenGL.ERROR_CHECKING = G.args.get('debugopengl', False)
OpenGL.ERROR_LOGGING = G.args.get('debugopengl', False)
OpenGL.FULL_LOGGING = G.args.get('fullloggingopengl', False)
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GL.ARB.texture_multisample import *
from . import normalize, findcontours


make_human_dir = 'D:/Python/human/makehuman/makehuman'

fileResult = make_human_dir + '/data/MyAutoData/'
filepath1 = make_human_dir + '/data/MyAutoData/ORIGINAL_MODEL.bvh'
fileout = make_human_dir + '/data/MyAutoData/OUTPUT_MODEL.bvh'
filepicbvh = make_human_dir + '/data/MyAutoData/MyPicture.bvh'
filepicture = make_human_dir + '/data/MyAutoData/picture.png'
sys.path.append(fileResult)

work_dir = make_human_dir + '/plugins/7_auto_human_pose/data/Auto3DImage/'

if os.path.exists(fileResult):
    pass
else:
    os.mkdir(fileResult)


class AotuPose1(gui3d.Action):
    def __init__(self, name, library, before, after):
        super(AotuPose1, self).__init__(name)
        self.library = library
        self.before = before
        self.after = after

    def do(self):
        self.library.loadPose(self.after)
        return True

    def undo(self):
        self.library.loadPose(self.before)
        return True


class PoseLibraryAotu1TaskView(gui3d.TaskView, filecache.MetadataCacher):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'AutoPose')
        # super(PoseLibraryAotu1TaskView, self).__init__(category, 'clothes', multiProxy = True, tagFilter = True)
        filecache.MetadataCacher.__init__(self, ['bvh'], 'pose_filecache.mhc')
        self.cache_format_version = '1c'  # Bump cacher version for updated format of pose metadata
        box1 = self.addLeftWidget(gui.GroupBox('ImageMatch'))
        self.aButtonC1 = box1.addWidget(gui.Button('L.UpArm'))
        self.aButtonC2 = box1.addWidget(gui.Button('L.LowArm'))
        self.aButtonC3 = box1.addWidget(gui.Button('R.UpArm'))
        self.aButtonC4 = box1.addWidget(gui.Button('R.LowArm'))
        self.aButtonC5 = box1.addWidget(gui.Button('L.UpLeg'))
        self.aButtonC6 = box1.addWidget(gui.Button('L.LowLeg'))
        self.aButtonC7 = box1.addWidget(gui.Button('R.UpLeg'))
        self.aButtonC8 = box1.addWidget(gui.Button('R.LowLeg'))
        box = self.addLeftWidget(gui.GroupBox('AngleRotate'))
        self.aSliderLabel = box.addWidget(gui.TextView('Value is initialize=0.5'))
        self.InitButton = box.addWidget(gui.Button('Init Pose'))

        @self.InitButton.mhEvent
        def onClicked(event):
            chushihua()
            bvhanniu()
            gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
            # gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, filepath1))
            # anim = self.loadBvh(fileout, convertFromZUp="auto")
            log.message("Init Pose.")

        self.aButton = box.addWidget(gui.Button('BVH'))
        #  self.aButton1 = box.addWidget(gui.Button('Save RGBImage'))
        self.aButton2 = box.addWidget(gui.Button('Save Image'))
        # self.aButton3 = box.addWidget(gui.Button('AotuPoseImage'))
        self.aSliderLabel = box.addWidget(gui.TextView('****************************'))
        a1 = [0]
        a2 = [0]
        a3 = [0]
        a4 = [0]
        a5 = [0]
        a6 = [0]
        a7 = [0]
        a8 = [0]
        deltvalue1 = [100]
        deltvalue2 = [100]
        deltvalue3 = [100]
        deltvalue4 = [100]
        deltvalue5 = [100]
        deltvalue6 = [100]
        deltvalue7 = [100]
        deltvalue8 = [100]
        deltva1 = [0]
        deltva2 = [0]
        deltva3 = [0]
        deltva4 = [0]
        deltva5 = [0]
        deltva6 = [0]
        deltva7 = [0]
        deltva8 = [0]
        self.aSlider = box.addWidget(gui.Slider(value=0.5, label=['upperarm01.L', ' %.3f']))

        @self.aSlider.mhEvent
        def onChange(value):
            self.aSliderLabel.setTextFormat('AngleRotate is %.1f', (value - 0.5) * 100)
            a1[0] = (value - 0.5) * 100
            bvhanniu()
            gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
            anim = self.loadBvh(fileout, convertFromZUp="auto")

        log.message(str(a1[0]))
        self.aSlider = box.addWidget(gui.Slider(value=0.5, label=['lowerarm01.L', ' %.3f']))

        # self.aSliderLabel = box.addWidget(gui.TextView('Value is initialize=0.5'))
        @self.aSlider.mhEvent
        def onChange(value):
            self.aSliderLabel.setTextFormat('AngleRotate is %.1f', (value - 0.5) * 100)
            # global a2
            a2[0] = (value - 0.5) * 100
            bvhanniu()
            gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
            anim = self.loadBvh(fileout, convertFromZUp="auto")
            # return a2

        # laL=onChange()
        self.aSlider = box.addWidget(gui.Slider(value=0.5, label=['upperarm01.R', ' %.3f']))

        #  self.aSliderLabel = box.addWidget(gui.TextView('Value is initialize=0.5'))
        @self.aSlider.mhEvent
        def onChange(value):
            self.aSliderLabel.setTextFormat('AngleRotate is %.1f', (value - 0.5) * 100)
            # global a3
            a3[0] = (value - 0.5) * 100
            bvhanniu()
            gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
            anim = self.loadBvh(fileout, convertFromZUp="auto")
            # return a3

        # ulL=onChange(value)
        self.aSlider = box.addWidget(gui.Slider(value=0.5, label=['lowerarm01.R', ' %.3f']))

        # self.aSliderLabel = box.addWidget(gui.TextView('Value is initialize=0.5'))
        @self.aSlider.mhEvent
        def onChange(value):
            self.aSliderLabel.setTextFormat('AngleRotate is %.1f', (value - 0.5) * 100)
            # global a4
            a4[0] = (value - 0.5) * 100
            bvhanniu()
            gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
            anim = self.loadBvh(fileout, convertFromZUp="auto")
            # return a4

        # llL=onChange(value)
        self.aSlider = box.addWidget(gui.Slider(value=0.5, label=['upperleg01.L', ' %.3f']))

        # self.aSliderLabel = box.addWidget(gui.TextView('Value is initialize=0.5'))
        @self.aSlider.mhEvent
        def onChange(value):
            self.aSliderLabel.setTextFormat('AngleRotate is %.1f', (value - 0.5) * 100)
            # global a5
            a5[0] = (value - 0.5) * 100
            bvhanniu()
            gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
            anim = self.loadBvh(fileout, convertFromZUp="auto")
            # return a5

        # uaR=onChange(value)
        self.aSlider = box.addWidget(gui.Slider(value=0.0, label=['lowerleg01.L', ' %.3f']))

        # self.aSliderLabel = box.addWidget(gui.TextView('Value is initialize=0.5'))
        @self.aSlider.mhEvent
        def onChange(value):
            self.aSliderLabel.setTextFormat('AngleRotate is %.1f', (value - 0.0) * 100)
            # global a6
            a6[0] = (value - 0.0) * 100
            bvhanniu()
            gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
            anim = self.loadBvh(fileout, convertFromZUp="auto")
            # return a6

        # laR=onChange(value)
        self.aSlider = box.addWidget(gui.Slider(value=0.5, label=['upperleg01.R', ' %.3f']))

        #  self.aSliderLabel = box.addWidget(gui.TextView('Value is initialize=0.5'))
        @self.aSlider.mhEvent
        def onChange(value):
            self.aSliderLabel.setTextFormat('AngleRotate is %.1f', (value - 0.5) * 100)
            # global a7
            a7[0] = (value - 0.5) * 100
            bvhanniu()
            gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
            anim = self.loadBvh(fileout, convertFromZUp="auto")
            # return a7；

        # ulR=onChange(value)
        self.aSlider = box.addWidget(gui.Slider(value=0.0, label=['lowerleg01.R', ' %.3f']))

        # self.aSliderLabel = box.addWidget(gui.TextView('Value is initialize=0.5'))
        @self.aSlider.mhEvent
        def onChange(value):
            self.aSliderLabel.setTextFormat('AngleRotate is %.1f', (value - 0.0) * 100)
            # global a8
            a8[0] = (value - 0.0) * 100
            bvhanniu()
            gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
            anim = self.loadBvh(fileout, convertFromZUp="auto")
            # return a8

        # llR=onChange(value)
        # We make the first one selected
        self.human = G.app.selectedHuman
        self.currentPose = None

        self.paths = [mh.getDataPath('Mydata'), mh.getSysDataPath('Mydata')]

        self.filechooser = self.addRightWidget(
            fc.IconListFileChooser(self.paths, ['bvh'], 'thumb', mh.getSysDataPath('poses/notfound.thumb'), name='Pose',
                                   noneItem=True))
        self.filechooser.setIconSize(50, 50)
        self.filechooser.enableAutoRefresh(False)

        # filepath0=[str(0)]
        @self.filechooser.mhEvent
        def onFileSelected(filename):
            gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, filename))
            if not filename:
                self.human.resetToRestPose()

            else:
                anim = self.loadBvh(filename, convertFromZUp="auto")

        self.filechooser.setFileLoadHandler(fc.TaggedFileLoader(self))
        self.addLeftWidget(self.filechooser.createTagFilter())
        log.message(self.paths)
        self.skelObj = None
        # filepath1=self.paths+'\\ORIGINAL_MODEL.bvh'
        # filepath1=filepath0[0]
        fp = open(filepath1, "rU")
        bvh1 = bvh.BVH()
        bvh2 = bvh1._BVH__expectKeyword('HIERARCHY', fp)
        words = bvh1._BVH__expectKeyword('ROOT', fp)
        rootJoint = bvh1.addRootJoint(words[1])
        bvh1._BVH__readJoint(bvh1.rootJoint, fp)
        self.convertFromZUp = bvh1._autoGuessCoordinateSystem()
        log.message("Automatically guessed coordinate system for BVH file %s (%s)" % (
        filepath1, "Z-up" if self.convertFromZUp else "Y-up"))
        if self.convertFromZUp:
            # Conversion needed: convert from Z-up to Y-up
            bvh1._BVH__cacheGetJoints()
            for joint in bvh1.jointslist:
                bvh1._BVH__calcPosition(joint, joint.offset)

        # Read motion
        bvh1._BVH__expectKeyword('MOTION', fp)
        words = bvh1._BVH__expectKeyword('Frames:', fp)
        self.frameCount = int(words[1])
        words = bvh1._BVH__expectKeyword('Frame', fp)  # Time:
        self.frameTime = float(words[2])

        for i in range(self.frameCount):
            line = fp.readline()
            words = line.split()
            data = [float(word) for word in words]
            if i != 43:
                for joint in bvh1.getJointsBVHOrder():
                    data = bvh1._BVH__processChannelData(joint, data)

            else:
                data = int(90)

        bvh1._BVH__cacheGetJoints()
        bvh1.frameCount = self.frameCount
        # Transform frame data into transformation matrices for all joints
        for joint in bvh1.getJoints():
            joint.calculateFrames()

        @self.aButtonC1.mhEvent
        def onClicked(event):
            chushihua()
            width = G.windowWidth;
            height = G.windowHeight;
            width = width - 3;
            height = height - 3;
            log.message(str(width))
            log.message(str(height))

            OrigalIm = cv2.imread(filepicture)  # 先读目标图像
            for value in range(0, 101, 20):
                a1[0] = value - 50
                bvhanniu()
                gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
                anim = self.loadBvh(fileout, convertFromZUp="auto")
                # cv2.waitKey(10)
                # filenameImage=fileResult+str(time.strftime("%Y-%m-%d_%H.%M.%S"))+'.png'
                filenameImage = fileResult + str(a1[0]) + 'DegreeLarm.png'
                # filenameIma=fileResult+str(time.strftime("%Y-%m-%d_%H.%M.%S"))+'.png'
                filenameIma = fileResult + str(a1[0]) + 'DegreeLarm.png'
                width = G.windowWidth;
                height = G.windowHeight;

                Xdel = 600  # 原图为800x600  减除后为200x150
                Ydel = 450
                width = width - Xdel;
                height = height - Ydel;
                # log.message(filenameImage)
                # mh.grabScreen(300,225,width,height,filenameImage)  #存盘

                mh.grabScreen(Xdel / 2, Ydel / 2, width, height, filenameImage)  # 不存盘，全在内在操作，提高速度
                log.message("Saved screengrab to %s", filenameImage)

                img = cv2.imread(filenameImage)  # 存盘
                height1, width1 = img.shape[:2]
                # print height,width
                for i in range(height1):
                    for j in range(width1):
                        r, b, g = img[i][j]
                        rb = abs(r - b)
                        rg = abs(r - g)
                        bg = abs(b - g)
                        if rb < 10 and rg < 10 and bg < 10:
                            img[i][j] = [0, 0, 0]
                        else:
                            img[i][j] = [255, 255, 255]

                imsave = normalize.Normalize(img)
                cv2.imwrite(filenameIma, imsave)
                # cv2.imshow("img",imsave)
                # cv2.waitKey(10)
                # delt1=findcontours.GetDeltValue(imsave,OrigalIm)  #onpicture()
                delt1 = findcontours.CalDiff(imsave, OrigalIm)
                log.debug('delt1 (%d Degree): = %f', a1[0], delt1)
                if delt1 <= deltvalue1[0]:
                    deltvalue1[0] = delt1
                    deltva1[0] = value - 50
                    filenameImaFit = filenameIma
                    bvhanniu(filepicbvh)
                    # gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, filepicbvh))
                    # anim = self.loadBvh(filepicbvh, convertFromZUp="auto")
                    imsavefit = imsave

            gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, filepicbvh))
            # anim = self.loadBvh(filepicbvh, convertFromZUp="auto")
            a1[0] = deltva1[0]  # 需要更新，不然后面姿态重置了
            bvhanniu()
            num1 = (deltva1[0] + 50) / 5
            # result=cv2.imread(fileResult+str(num1)+'.png')
            # result=cv2.imread(filenameImaFit)
            result = imsavefit
            result2 = cv2.imread(filepicture)
            cv2.imshow("Result", result)
            cv2.imshow("Original", result2)
            # cv2.waitKey(10)
            log.message(deltvalue1)
            log.message(num1)
            imsavefit = None

        @self.aButtonC2.mhEvent
        def onClicked(event):
            chushihua()
            width = G.windowWidth;
            height = G.windowHeight;
            width = width - 3;
            height = height - 3;
            log.message(str(width))
            log.message(str(height))
            for value in range(5, 100, 5):
                a2[0] = value - 50
                bvhanniu()
                gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
                # anim = self.loadBvh(fileout, convertFromZUp="auto")
                filenameImage = work_dir + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
                filenameIma = work_dir + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
                width = G.windowWidth;
                height = G.windowHeight;
                width = width - 3;
                height = height - 3;
                # log.message(filenameImage)
                mh.grabScreen(0, 0, width, height, filenameImage)
                img = cv2.imread(filenameImage)
                height1, width1 = img.shape[:2]
                # print height,width
                for i in range(height1):
                    for j in range(width1):
                        r, b, g = img[i][j]
                        rb = abs(r - b)
                        rg = abs(r - g)
                        bg = abs(b - g)
                        if rb < 10 and rg < 10 and bg < 10:
                            img[i][j] = [0, 0, 0]
                        else:
                            img[i][j] = [255, 255, 255]

                imsave = normalize.Normalize(img)
                cv2.imwrite(filenameIma, imsave)
                cv2.imshow("img", imsave)
                cv2.waitKey(10)
                delt2 = onpicture()
                if delt2 <= deltvalue2[0]:
                    deltvalue2[0] = delt2
                    deltva2[0] = value - 50

            num2 = (deltva2[0] + 50) / 5
            result = cv2.imread(fileResult + str(num2) + '.png')
            cv2.imshow("Result", result)
            cv2.waitKey(0)
            log.message(deltvalue2)
            log.message(num2)

        @self.aButtonC3.mhEvent
        def onClicked(event):
            chushihua()
            width = G.windowWidth;
            height = G.windowHeight;
            width = width - 3;
            height = height - 3;
            log.message(str(width))
            log.message(str(height))
            for value in range(5, 100, 5):
                a3[0] = value - 50
                bvhanniu()
                gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
                # anim = self.loadBvh(fileout, convertFromZUp="auto")
                filenameImage = work_dir + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
                filenameIma = work_dir + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
                width = G.windowWidth;
                height = G.windowHeight;
                width = width - 3;
                height = height - 3;
                # log.message(filenameImage)
                mh.grabScreen(0, 0, width, height, filenameImage)
                img = cv2.imread(filenameImage)
                height1, width1 = img.shape[:2]
                # print height,width
                for i in range(height1):
                    for j in range(width1):
                        r, b, g = img[i][j]
                        rb = abs(r - b)
                        rg = abs(r - g)
                        bg = abs(b - g)
                        if rb < 10 and rg < 10 and bg < 10:
                            img[i][j] = [0, 0, 0]
                        else:
                            img[i][j] = [255, 255, 255]

                imsave = normalize.Normalize(img)
                cv2.imwrite(filenameIma, imsave)
                cv2.imshow("img", imsave)
                cv2.waitKey(10)
                delt3 = onpicture()
                if delt3 <= deltvalue3[0]:
                    deltvalue3[0] = delt3
                    deltva3[0] = value - 50

            num3 = (deltva3[0] + 50) / 5
            result = cv2.imread(fileResult + str(num3) + '.png')
            cv2.imshow("Result", result)
            cv2.waitKey(0)
            log.message(deltvalue3)
            log.message(num3)

        @self.aButtonC4.mhEvent
        def onClicked(event):
            chushihua()
            width = G.windowWidth;
            height = G.windowHeight;
            width = width - 3;
            height = height - 3;
            log.message(str(width))
            log.message(str(height))
            for value in range(5, 100, 5):
                a4[0] = value - 50
                bvhanniu()
                gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
                # anim = self.loadBvh(fileout, convertFromZUp="auto")
                filenameImage = work_dir + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
                filenameIma = work_dir + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
                width = G.windowWidth;
                height = G.windowHeight;
                width = width - 3;
                height = height - 3;
                # log.message(filenameImage)
                mh.grabScreen(0, 0, width, height, filenameImage)
                img = cv2.imread(filenameImage)
                height1, width1 = img.shape[:2]
                # print height,width
                for i in range(height1):
                    for j in range(width1):
                        r, b, g = img[i][j]
                        rb = abs(r - b)
                        rg = abs(r - g)
                        bg = abs(b - g)
                        if rb < 10 and rg < 10 and bg < 10:
                            img[i][j] = [0, 0, 0]
                        else:
                            img[i][j] = [255, 255, 255]

                imsave = normalize.Normalize(img)
                cv2.imwrite(filenameIma, imsave)
                cv2.imshow("img", imsave)
                cv2.waitKey(10)
                delt4 = onpicture()
                if delt4 <= deltvalue4[0]:
                    deltvalue4[0] = delt4
                    deltva4[0] = value - 50

            num4 = (deltva4[0] + 50) / 5
            result = cv2.imread(fileResult + str(num4) + '.png')
            cv2.imshow("Result", result)
            cv2.waitKey(0)
            log.message(deltvalue4)
            log.message(num4)

        @self.aButtonC5.mhEvent
        def onClicked(event):
            width = G.windowWidth;
            height = G.windowHeight;
            width = width - 3;
            height = height - 3;
            log.message(str(width))
            log.message(str(height))
            for value in range(5, 100, 5):
                chushihua()
                a5[0] = value - 50
                bvhanniu()
                gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
                # anim = self.loadBvh(fileout, convertFromZUp="auto")
                filenameImage = work_dir + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
                filenameIma = work_dir + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
                width = G.windowWidth;
                height = G.windowHeight;
                width = width - 3;
                height = height - 3;
                # log.message(filenameImage)
                mh.grabScreen(0, 0, width, height, filenameImage)
                img = cv2.imread(filenameImage)
                height1, width1 = img.shape[:2]
                # print height,width
                for i in range(height1):
                    for j in range(width1):
                        r, b, g = img[i][j]
                        rb = abs(r - b)
                        rg = abs(r - g)
                        bg = abs(b - g)
                        if rb < 10 and rg < 10 and bg < 10:
                            img[i][j] = [0, 0, 0]
                        else:
                            img[i][j] = [255, 255, 255]

                imsave = normalize.Normalize(img)
                cv2.imwrite(filenameIma, imsave)
                cv2.imshow("img", imsave)
                cv2.waitKey(10)
                delt5 = onpicture()
                if delt5 <= deltvalue5[0]:
                    deltvalue5[0] = delt5
                    deltva5[0] = value - 50

            num5 = (deltva5[0] + 50) / 5
            result = cv2.imread(fileResult + str(num5) + '.png')
            cv2.imshow("Result", result)
            cv2.waitKey(0)
            log.message(deltvalue5)
            log.message(num5)

        @self.aButtonC6.mhEvent
        def onClicked(event):
            # chushihua()
            width = G.windowWidth;
            height = G.windowHeight;
            width = width - 3;
            height = height - 3;
            log.message(str(width))
            log.message(str(height))

            OrigalIm = cv2.imread(filepicture)  # 先读目标图像
            for value in range(49, 101, 10):
                a6[0] = value - 50
                bvhanniu()
                gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
                # anim = self.loadBvh(fileout, convertFromZUp="auto")
                # cv2.waitKey(10)
                # filenameImage=fileResult+str(time.strftime("%Y-%m-%d_%H.%M.%S"))+'.png'
                filenameImage = fileResult + str(a6[0]) + 'DegreeLLeg.png'
                # filenameIma=fileResult+str(time.strftime("%Y-%m-%d_%H.%M.%S"))+'.png'
                filenameIma = fileResult + str(a6[0]) + 'DegreeLLeg.png'
                width = G.windowWidth;
                height = G.windowHeight;

                Xdel = 600  # 原图为800x600  减除后为200x150
                Ydel = 450
                width = width - Xdel;
                height = height - Ydel;
                # log.message(filenameImage)
                # mh.grabScreen(300,225,width,height,filenameImage)  #存盘

                mh.grabScreen(Xdel / 2, Ydel / 2, width, height, filenameImage)  # 不存盘，全在内在操作，提高速度
                log.message("Saved screengrab to %s", filenameImage)

                img = cv2.imread(filenameImage)  # 存盘
                height1, width1 = img.shape[:2]
                # print height,width
                for i in range(height1):
                    for j in range(width1):
                        r, b, g = img[i][j]
                        rb = abs(r - b)
                        rg = abs(r - g)
                        bg = abs(b - g)
                        if rb < 10 and rg < 10 and bg < 10:
                            img[i][j] = [0, 0, 0]
                        else:
                            img[i][j] = [255, 255, 255]

                imsave = normalize.Normalize(img)
                cv2.imwrite(filenameIma, imsave)
                # cv2.imshow("img",imsave)
                # cv2.waitKey(10)
                # delt6=findcontours.GetDeltValue(imsave,OrigalIm)  #onpicture()
                delt6 = findcontours.CalDiff(imsave, OrigalIm)
                log.debug('delt6 (%d Degree): = %f', a6[0], delt6)
                if delt6 <= deltvalue6[0]:
                    deltvalue6[0] = delt6
                    deltva6[0] = value - 50
                    filenameImaFit = filenameIma
                    bvhanniu(filepicbvh)
                    # gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, filepicbvh))
                    # anim = self.loadBvh(filepicbvh, convertFromZUp="auto")
                    imsavefit = imsave

            gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, filepicbvh))
            anim = self.loadBvh(filepicbvh, convertFromZUp="auto")
            a6[0] = deltva6[0]  # 需要更新，不然后面姿态重置了
            bvhanniu()
            num1 = (deltva6[0] + 50) / 5
            # result=cv2.imread(fileResult+str(num1)+'.png')
            # result=cv2.imread(filenameImaFit)
            result = imsavefit
            result2 = cv2.imread(filepicture)
            cv2.imshow("Result", result)
            cv2.imshow("Original", result2)
            # cv2.waitKey(10)
            log.message(deltvalue6)
            log.message(num1)
            imsavefit = None

        @self.aButtonC7.mhEvent
        def onClicked(event):
            # chushihua()
            width = G.windowWidth;
            height = G.windowHeight;
            width = width - 3;
            height = height - 3;
            log.message(str(width))
            log.message(str(height))

            OrigalIm = cv2.imread(filepicture)  # 先读目标图像
            for value in range(0, 60, 10):
                a7[0] = value - 50
                bvhanniu()
                gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
                anim = self.loadBvh(fileout, convertFromZUp="auto")
                # cv2.waitKey(10)
                # filenameImage=fileResult+str(time.strftime("%Y-%m-%d_%H.%M.%S"))+'.png'
                filenameImage = fileResult + str(a7[0]) + 'DegreeLLeg.png'
                # filenameIma=fileResult+str(time.strftime("%Y-%m-%d_%H.%M.%S"))+'.png'
                filenameIma = fileResult + str(a7[0]) + 'DegreeLLeg.png'
                width = G.windowWidth;
                height = G.windowHeight;

                Xdel = 600  # 原图为800x600  减除后为200x150
                Ydel = 450
                width = width - Xdel;
                height = height - Ydel;
                # log.message(filenameImage)
                # mh.grabScreen(300,225,width,height,filenameImage)  #存盘

                mh.grabScreen(Xdel / 2, Ydel / 2, width, height, filenameImage)  # 不存盘，全在内在操作，提高速度
                log.message("Saved screengrab to %s", filenameImage)

                img = cv2.imread(filenameImage)  # 存盘
                height1, width1 = img.shape[:2]
                # print height,width
                for i in range(height1):
                    for j in range(width1):
                        r, b, g = img[i][j]
                        rb = abs(r - b)
                        rg = abs(r - g)
                        bg = abs(b - g)
                        if rb < 10 and rg < 10 and bg < 10:
                            img[i][j] = [0, 0, 0]
                        else:
                            img[i][j] = [255, 255, 255]

                imsave = normalize.Normalize(img)
                cv2.imwrite(filenameIma, imsave)
                # cv2.imshow("img",imsave)
                # cv2.waitKey(10)
                # delt7=findcontours.GetDeltValue(imsave,OrigalIm)  #onpicture()
                delt7 = findcontours.CalDiff(imsave, OrigalIm)
                log.debug('delt7 (%d Degree): = %f', a7[0], delt7)
                if delt7 <= deltvalue7[0]:
                    deltvalue7[0] = delt7
                    deltva7[0] = value - 50
                    filenameImaFit = filenameIma
                    bvhanniu(filepicbvh)
                    # gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, filepicbvh))
                    anim = self.loadBvh(filepicbvh, convertFromZUp="auto")
                    imsavefit = imsave

            gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, filepicbvh))
            anim = self.loadBvh(filepicbvh, convertFromZUp="auto")
            a7[0] = deltva7[0]  # 需要更新，不然后面姿态重置了
            bvhanniu()
            num1 = (deltva7[0] + 50) / 5
            # result=cv2.imread(fileResult+str(num1)+'.png')
            # result=cv2.imread(filenameImaFit)
            result = imsavefit
            result2 = cv2.imread(filepicture)
            cv2.imshow("Result", result)
            cv2.imshow("Original", result2)
            # cv2.waitKey(10)
            log.message(deltvalue7)
            log.message(num1)
            imsavefit = None

        @self.aButtonC8.mhEvent
        def onClicked(event):
            # chushihua()
            width = G.windowWidth;
            height = G.windowHeight;
            width = width - 3;
            height = height - 3;
            log.message(str(width))
            log.message(str(height))

            OrigalIm = cv2.imread(filepicture)  # 先读目标图像
            for value in range(61, 71, 10):
                a8[0] = value - 50
                bvhanniu()
                gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, fileout))
                anim = self.loadBvh(fileout, convertFromZUp="auto")
                # cv2.waitKey(10)
                # filenameImage=fileResult+str(time.strftime("%Y-%m-%d_%H.%M.%S"))+'.png'
                filenameImage = fileResult + str(a8[0]) + 'DegreeLLeg.png'
                # filenameIma=fileResult+str(time.strftime("%Y-%m-%d_%H.%M.%S"))+'.png'
                filenameIma = fileResult + str(a8[0]) + 'DegreeLLeg.png'
                width = G.windowWidth;
                height = G.windowHeight;

                Xdel = 600  # 原图为800x600  减除后为200x150
                Ydel = 450
                width = width - Xdel;
                height = height - Ydel;
                # log.message(filenameImage)
                # mh.grabScreen(300,225,width,height,filenameImage)  #存盘

                mh.grabScreen(Xdel / 2, Ydel / 2, width, height, filenameImage)  # 不存盘，全在内在操作，提高速度
                log.message("Saved screengrab to %s", filenameImage)

                img = cv2.imread(filenameImage)  # 存盘
                height1, width1 = img.shape[:2]
                # print height,width
                for i in range(height1):
                    for j in range(width1):
                        r, b, g = img[i][j]
                        rb = abs(r - b)
                        rg = abs(r - g)
                        bg = abs(b - g)
                        if rb < 10 and rg < 10 and bg < 10:
                            img[i][j] = [0, 0, 0]
                        else:
                            img[i][j] = [255, 255, 255]

                imsave = normalize.Normalize(img)
                cv2.imwrite(filenameIma, imsave)
                # cv2.imshow("img",imsave)
                # cv2.waitKey(10)
                # delt8=findcontours.GetDeltValue(imsave,OrigalIm)  #onpicture()
                delt8 = findcontours.CalDiff(imsave, OrigalIm)
                log.debug('delt8 (%d Degree): = %f', a8[0], delt8)
                if delt8 <= deltvalue8[0]:
                    deltvalue8[0] = delt8
                    deltva8[0] = value - 50
                    filenameImaFit = filenameIma
                    bvhanniu(filepicbvh)
                    gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, filepicbvh))
                    anim = self.loadBvh(filepicbvh, convertFromZUp="auto")
                    imsavefit = imsave

            gui3d.app.do(AotuPose1("Change pose", self, self.currentPose, filepicbvh))
            anim = self.loadBvh(filepicbvh, convertFromZUp="auto")
            a8[0] = deltva8[0]  # 需要更新，不然后面姿态重置了
            bvhanniu()
            num1 = (deltva8[0] + 50) / 5
            # result=cv2.imread(fileResult+str(num1)+'.png')
            # result=cv2.imread(filenameImaFit)
            result = imsavefit
            result2 = cv2.imread(filepicture)
            cv2.imshow("Result", result)
            cv2.imshow("Original", result2)
            # cv2.waitKey(10)
            log.message(deltvalue8)
            log.message(num1)
            imsavefit = None

        def chushihua():
            a1 = [0]
            a2 = [0]
            a3 = [0]
            a4 = [0]
            a5 = [0]
            a6 = [0]
            a7 = [0]
            a8 = [0]
            deltvalue1 = [100]
            deltvalue2 = [100]
            deltvalue3 = [100]
            deltvalue4 = [100]
            deltvalue5 = [100]
            deltvalue6 = [100]
            deltvalue7 = [100]
            deltvalue8 = [100]
            deltva1 = [0]
            deltva2 = [0]
            deltva3 = [0]
            deltva4 = [0]
            deltva5 = [0]
            deltva6 = [0]
            deltva7 = [0]
            deltva8 = [0]

        def bvhanniu(filename=None):
            if filename is None:
                filename = fileout
            log.debug('FileName is %s', filename)
            f = open(filename, 'w')
            # Write structure
            f.write('HIERARCHY\n')
            bvh1._writeJoint(f, bvh1.rootJoint, 0)
            # Write animation
            f.write('MOTION\n')
            f.write('Frames: %s\n' % bvh1.frameCount)
            f.write('Frame Time: %f\n' % bvh1.frameTime)
            allJoints = [joint for joint in bvh1.getJointsBVHOrder() if not joint.isEndConnector()]
            jointsData = [joint.matrixPoses for joint in allJoints]
            nJoints = len(jointsData)
            nFrames = len(jointsData[0])
            totalChannels = sum([len(joint.channels) for joint in allJoints])

            frameData = []
            for fIdx in range(bvh1.frameCount):
                for joint in allJoints:
                    offset = fIdx * len(joint.channels)
                    frameData.extend(joint.frames[offset:offset + len(joint.channels)])
                frameData = [str(fl) for fl in frameData]

            frameData[37] = str(a1[0])
            frameData[43] = str(a2[0] + 35)
            frameData[127] = str(a3[0])
            frameData[133] = str(a4[0] + 35)
            frameData[433] = str(a5[0])
            frameData[439] = str(a6[0])
            frameData[508] = str(a7[0])
            frameData[514] = str(a8[0])
            for fIdx in range(bvh1.frameCount):
                frameData = [str(fl) for fl in frameData]
                f.write('%s\n' % " ".join(frameData))

            f.close()

        # @self.aButton1.mhEvent
        # def onClicked(event):
        #  filenameImage='F:/'+str(time.strftime("%Y-%m-%d_%H.%M.%S"))+'.png'
        # width = G.windowWidth;
        #   height = G.windowHeight;
        #  width = width - 3;
        #  height = height - 3;
        #  log.message(filenameImage)
        #  mh.grabScreen(0,0,width,height,filenameImage)
        def dayinpicture():
            filenameImage = work_dir + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
            filenameIma = work_dir + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
            width = G.windowWidth;
            height = G.windowHeight;
            width = width - 3;
            height = height - 3;
            # log.message(filenameImage)
            # mh.grabScreen(0,0,width,height,filenameImage)
            # img=cv2.imread(filenameImage)
            img = grabMyScreen(0, 0, width, height)
            height1, width1 = img.shape[:2]
            # print height,width
            for i in range(height1):
                for j in range(width1):
                    r, b, g = img[i][j]
                    rb = abs(r - b)
                    rg = abs(r - g)
                    bg = abs(b - g)
                    if rb < 10 and rg < 10 and bg < 10:
                        img[i][j] = [0, 0, 0]
                    else:
                        img[i][j] = [255, 255, 255]

            imsave = normalize.Normalize(img)
            cv2.imwrite(filenameIma, imsave)

        @self.aButton2.mhEvent
        def onClicked(event):
            filenameImage = work_dir + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
            filenameIma = work_dir + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
            width = G.windowWidth;
            height = G.windowHeight;
            width = width - 3;
            height = height - 3;
            log.message(filenameImage)
            mh.grabScreen(0, 0, width, height, filenameImage)
            img = cv2.imread(filenameImage)
            height1, width1 = img.shape[:2]
            # print height,width
            for i in range(height1):
                for j in range(width1):
                    r, b, g = img[i][j]
                    rb = abs(r - b)
                    rg = abs(r - g)
                    bg = abs(b - g)
                    if rb < 10 and rg < 10 and bg < 10:
                        img[i][j] = [0, 0, 0]
                    else:
                        img[i][j] = [255, 255, 255]

            cv2.imwrite(filenameIma, img)

        # getcontourspoint.MainGetContourPoint(filenameImage,"F:/w1/lunkuo.txt")

        def onpicture():
            filenameImage = work_dir + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
            filenameIma = work_dir + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
            width = G.windowWidth;
            height = G.windowHeight;
            width = width - 3;
            height = height - 3;
            log.message(filenameImage)
            # mh.grabScreen(0,0,width,height,filenameImage)
            img = grabMyScreen(0, 0, width, height)
            # log.message(str(imgs))
            # img=cv2.imread(filenameImage)
            height1, width1 = img.shape[:2]
            # print height,width
            for i in range(height1):
                for j in range(width1):
                    r, b, g = img[i][j]
                    rb = abs(r - b)
                    rg = abs(r - g)
                    bg = abs(b - g)
                    if rb < 10 and rg < 10 and bg < 10:
                        img[i][j] = [0, 0, 0]
                    else:
                        img[i][j] = [255, 255, 255]

            # cv2.imwrite(filenameIma,img)
            imsave = normalize.Normalize(img)
            delt = findcontours.GetDeltValue(imsave, filepicture)
            return delt

        def grabMyScreen(x, y, width, height, filename=None, productionRender=False):
            if width <= 0 or height <= 0:
                raise RuntimeError("width or height is 0")

            log.debug('grabScreen: %d %d %d %d', x, y, width, height)

            # Draw before grabbing, to make sure we grab a rendering and not a picking buffer
            glmodule.draw(productionRender)

            sx0 = x
            sy0 = G.windowHeight - y - height
            sx1 = sx0 + width
            sy1 = sy0 + height

            sx0 = max(sx0, 0)
            sx1 = min(sx1, G.windowWidth)
            sy0 = max(sy0, 0)
            sy1 = min(sy1, G.windowHeight)

            rwidth = sx1 - sx0
            rwidth -= rwidth % 4
            sx1 = sx0 + rwidth
            rheight = sy1 - sy0

            surface = np.empty((rheight, rwidth, 3), dtype=np.uint8)

            log.debug('glReadPixels: %d %d %d %d', sx0, sy0, rwidth, rheight)

            glmodule.glReadPixels(sx0, sy0, rwidth, rheight, GL_RGB, GL_UNSIGNED_BYTE, surface)

            if width != rwidth or height != rheight:
                surf = np.zeros((height, width, 3), dtype=np.uint8) + 127
                surf[...] = surface[:1, :1, :]
                dx0 = (width - rwidth) / 2
                dy0 = (height - rheight) / 2
                dx1 = dx0 + rwidth
                dy1 = dy0 + rheight
                surf[dy0:dy1, dx0:dx1] = surface
                surface = surf

            surface = np.ascontiguousarray(surface[::-1, :, :])
            # surface = Image(data = surface)
            return surface

        @self.aButton.mhEvent
        def onClicked(event):
            f = open(filepath1, 'w')
            # Write structure
            f.write('HIERARCHY\n')
            bvh1._writeJoint(f, bvh1.rootJoint, 0)
            # Write animation
            f.write('MOTION\n')
            f.write('Frames: %s\n' % bvh1.frameCount)
            f.write('Frame Time: %f\n' % bvh1.frameTime)
            allJoints = [joint for joint in bvh1.getJointsBVHOrder() if not joint.isEndConnector()]
            jointsData = [joint.matrixPoses for joint in allJoints]
            nJoints = len(jointsData)
            nFrames = len(jointsData[0])
            totalChannels = sum([len(joint.channels) for joint in allJoints])
            frameData = []
            for fIdx in range(bvh1.frameCount):
                for joint in allJoints:
                    offset = fIdx * len(joint.channels)
                    frameData.extend(joint.frames[offset:offset + len(joint.channels)])
                frameData = [str(fl) for fl in frameData]

            for fIdx in range(bvh1.frameCount):
                frameData = [str(fl) for fl in frameData]
                f.write('%s\n' % " ".join(frameData))

            f.close()

    def getMetadataFile(self, filename):
        metafile = os.path.splitext(filename)[0] + '.meta'
        if os.path.isfile(metafile):
            return metafile
        return filename

    def getMetadataImpl(self, filename):
        tags = set()
        if not os.path.isfile(filename):
            return (tags,)
        name = os.path.splitext(os.path.basename(filename))[0]
        description = ""
        license = mh.getAssetLicense()
        from codecs import open
        f = open(filename, encoding='utf-8')
        for l in f.read().split('\n'):
            l = l.strip()
            l = l.split()
            if len(l) == 0:
                continue
            if l[0].lower() == 'tag':
                tags.add((' '.join(l[1:])).lower())
            elif l[0].lower() == 'name':
                name = ' '.join(l[1:])
            elif l[0].lower() == 'description':
                description = ' '.join(l[1:])
            elif l[0].lower() == 'author':
                license.author = ' '.join(l[1:])
            elif l[0].lower() == 'license':
                license.license = ' '.join(l[1:])
            elif l[0].lower() == 'copyright':
                license.copyright = ' '.join(l[1:])
            elif l[0].lower() == 'homepage':
                license.homepage = ' '.join(l[1:])
        return (tags, name, description, license)

    def getTagsFromMetadata(self, metadata):
        return metadata[0]

    def getSearchPaths(self):
        return self.paths

    def loadPose(self, filepath, apply_pose=True):
        self.currentPose = filepath

        if not filepath:
            self.human.resetToRestPose()
            return

        if os.path.splitext(filepath)[1].lower() == '.mhp':
            anim = self.loadMhp(filepath)
        elif os.path.splitext(filepath)[1].lower() == '.bvh':
            anim = self.loadBvh(filepath, convertFromZUp="auto")
        else:
            log.error("Cannot load pose file %s: File type unknown." % filepath)
            return

        # self.human.setAnimateInPlace(True)
        self.human.addAnimation(anim)
        self.human.setActiveAnimation(anim.name)
        self.human.setToFrame(0, update=False)
        if apply_pose:
            self.human.setPosed(True)

    def loadMhp(self, filepath):
        return animation.loadPoseFromMhpFile(filepath, self.human.getBaseSkeleton())

    def loadBvh(self, filepath, convertFromZUp="auto"):
        bvh_file = bvh.load(filepath, convertFromZUp)
        self.autoScaleBVH(bvh_file)
        anim = bvh_file.createAnimationTrack(self.human.getBaseSkeleton())
        _, _, _, license = self.getMetadata(filepath)
        anim.license = license
        return anim

    def autoScaleBVH(self, bvh_file):
        """
        Auto scale BVH translations by comparing upper leg length
        """
        import numpy.linalg as la
        COMPARE_BONE = "upperleg02.L"
        if COMPARE_BONE not in bvh_file.joints:
            raise RuntimeError('Failed to auto scale BVH file %s, it does not contain a joint for "%s"' % (
            bvh_file.name, COMPARE_BONE))
        bvh_joint = bvh_file.joints[COMPARE_BONE]
        bone = self.human.getBaseSkeleton().getBoneByReference(COMPARE_BONE)
        if bone is not None:
            joint_length = la.norm(bvh_joint.children[0].position - bvh_joint.position)
            scale_factor = bone.length / joint_length
            log.message("Scaling BVH file %s with factor %s" % (bvh_file.name, scale_factor))
            bvh_file.scale(scale_factor)
        else:
            log.warning(
                "Could not find bone or bone reference with name %s in skeleton %s, cannot auto resize BVH file %s",
                COMPARE_BONE, self.human.getBaseSkeleton().name, bvh_file.name)

    def onShow(self, event):
        self.filechooser.refresh()
        self.filechooser.selectItem(self.currentPose)
        self.human.refreshPose()

    def onHide(self, event):
        gui3d.app.statusPersist('')

    def onHumanChanging(self, event):
        if event.change == 'reset':
            self.human.removeAnimations(update=False)
            self.currentPose = None

    def onHumanChanged(self, event):
        if event.change == 'skeleton':
            if self.currentPose:
                self.loadPose(self.currentPose, apply_pose=False)
        elif event.change == 'reset':
            # Update GUI after reset (if tab is currently visible)
            if self.isShown():
                self.onShow(event)

    def loadHandler(self, human, values, strict):
        if values[0] == "pose":
            poseFile = values[1]
            poseFile = getpath.thoroughFindFile(poseFile, self.paths)
            if not os.path.isfile(poseFile):
                if strict:
                    raise RuntimeError("Could not load pose %s, file does not exist." % poseFile)
                log.warning("Could not load pose %s, file does not exist.", poseFile)
            else:
                self.loadPose(poseFile)
            return

    def saveHandler(self, human, file):
        if self.currentPose:
            poseFile = getpath.getRelativePath(self.currentPose, self.paths)
            file.write('pose %s\n' % poseFile)


category = None
taskview = None


# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements
def load(app):
    global taskview
    category = app.getCategory('Utilities')
    taskview = PoseLibraryAotu1TaskView(category)
    taskview.sortOrder = 2
    category.addTask(taskview)

    app.addLoadHandler('pose', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler, priority=6)  # After skeleton library


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements
def unload(app):
    taskview.onUnload()
