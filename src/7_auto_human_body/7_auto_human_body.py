# -*- coding: utf-8 -*-
import sys
import time
import glmodule
import numpy as np
import cv2
import os
import log
import mh
import OpenGL
import gui
import gui3d
import humanmodifier
import modifierslider
from collections import OrderedDict
from core import G

OpenGL.ERROR_CHECKING = G.args.get('debugopengl', False)
OpenGL.ERROR_LOGGING = G.args.get('debugopengl', False)
OpenGL.FULL_LOGGING = G.args.get('fullloggingopengl', False)
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GL.ARB.texture_multisample import *

#fileStartDir = os.path.abspath(os.path.dirname('7_auto_human_body.py'))+'/plugins'
# make_human_path = '/usr/share/makehuman'
make_human_path = 'D:/Python/human/makehuman/makehuman'
fileStartDir = make_human_path + '/plugins/7_auto_human_body'
fileAutoData = fileStartDir + '/data/MyAutoData'
fileResult = fileStartDir + '/data/MyAutoData/'
filepicture = fileStartDir + '/data/MyAutoData/picture.png'
# sys.path.append(fileAutoData)
from . import normalize, findcontours

fileAotupicture = fileStartDir + "/data/Auto3DImage"
if os.path.exists(fileAotupicture):
    pass
else:
    os.mkdir(fileAotupicture)


class Modifier1TaskView(gui3d.TaskView):
    def __init__(self, category, name, label=None, saveName=None, cameraView=None):
        if label is None:
            label = name.capitalize()
        if saveName is None:
            saveName = name

        super(Modifier1TaskView, self).__init__(category, name, label=label)

        self.saveName = saveName
        self.cameraFunc = _getCamFunc(cameraView)

        self.groupBoxes = OrderedDict()
        self.radioButtons = []
        self.sliders = []
        self.modifiers = {}

        self.categoryBox = self.addRightWidget(gui.GroupBox('Category'))
        self.groupBox = self.addLeftWidget(gui.StackedBox())

        self.showMacroStats = False
        self.human = gui3d.app.selectedHuman
        a = [0]
        deltvalue = [100]
        deltva = [0]
        box = self.addLeftWidget(gui.GroupBox(u'体态自动化'))
        self.aButton = box.addWidget(gui.Button(u'体态变化'))

        @self.aButton.mhEvent
        def onClicked(event):
            log.message('start...')
            for slider in self.sliders:
                for valuenum in range(0, 105, 5):
                    valuenums = valuenum / 100.000000
                    slider.update()
                    # log.message(slider.modifier.getValue())
                    # if slider.enabledCondition:
                    # log.message(slider)
                    slider.modifier.setValue(valuenums)
                    # log.message(slider.modifier.getValue())
                    sli = modifierslider.ModifierSlider(slider.modifier)
                    value = slider.modifier.getValue()
                    valuesli = sli.getValue()
                    # sli.onChanging(slider.modifier.getValue())
                    action = humanmodifier.ModifierAction(slider.modifier, value, valuesli, sli.update)
                    log.message(str(valuesli))
                    log.message(str(value))
                    if valuesli != value:
                        G.app.do(action)
                    else:
                        action.do()

                    filenameImage = fileAotupicture + '/' + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
                    filenameIma = fileAotupicture + '/' + str(time.strftime("%Y-%m-%d_%H.%M.%S")) + '.png'
                    filenameIma1 = fileAotupicture + '/result' + str(time.strftime("%Y-%m-%d_%H.%M.%S")), '.png'
                    width = G.windowWidth;
                    height = G.windowHeight;
                    width1 = width - 3;
                    height1 = height - 3;
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
                    # cv2.imshow("img",imsave)
                    # cv2.waitKey(10)
                    delt = onpicture()
                    log.message(str(delt))
                    if delt <= deltvalue[0]:
                        deltvalue[0] = delt
                        deltva[0] = valuenums

                num = deltva[0] * 20 + 1
                result = cv2.imread(fileResult + str(num) + '.png')
                cv2.imshow("Result", result)
                cv2.waitKey(0)
                log.message(deltvalue)
                log.message(num)

            slider.modifier.setValue(valuenums)
            # log.message(slider.modifier.getValue())
            sli = modifierslider.ModifierSlider(slider.modifier)
            value = slider.modifier.getValue()
            valuesli = sli.getValue()
            # sli.onChanging(slider.modifier.getValue())
            action = humanmodifier.ModifierAction(slider.modifier, value, valuesli, sli.update)
            G.app.do(action)
            mh.grabScreen(0, 0, width, height, filenameImage)
            imgw = cv2.imread(filenameImage)
            height1, width1 = imgw.shape[:2]
            # print height,width
            for i in range(height1):
                for j in range(width1):
                    r, b, g = imgw[i][j]
                    rb = abs(r - b)
                    rg = abs(r - g)
                    bg = abs(b - g)
                    if rb < 10 and rg < 10 and bg < 10:
                        imgw[i][j] = [0, 0, 0]
                    else:
                        imgw[i][j] = [255, 255, 255]

            imsavew = normalize.Normalize(imgw)
            cv2.imwrite(filenameIma1, imsavew)
            # sli.resetValue()
            # syncSliders()
            # slider.modifier.human
            # enabled = getattr(slider.modifier.human, slider.enabledCondition)()
            # slider.setEnabled(str(2))
            # log.message(str(enabled))

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

        def onpicture():
            # filenameImage='F:/Auto3DImage/'+str(time.strftime("%Y-%m-%d_%H.%M.%S"))+'.png'
            # filenameIma='F:/Auto3DImage/'+str(time.strftime("%Y-%m-%d_%H.%M.%S"))+'.png'
            width = G.windowWidth;
            height = G.windowHeight;
            width = width - 3;
            height = height - 3;
            # log.message(filenameImage)
            # mh.grabScreen(0,0,width,height,filenameImage)
            img = grabMyScreen(0, 0, width, height)
            # log.message(str(imgs))
            # img=cv2.imread(filenameImage)
            height, width = img.shape[:2]
            # print height,width
            for i in range(height):
                for j in range(width):
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
            imnew= cv2.imread(filepicture)
            delt = findcontours.GetDeltValue(imsave, imnew)
            return delt

    def addSlider(self, sliderCategory, slider, enabledCondition=None):
        # Get category groupbox
        categoryName = sliderCategory.capitalize()
        if categoryName not in self.groupBoxes:
            # Create box
            box = self.groupBox.addWidget(gui.GroupBox(categoryName))
            self.groupBoxes[categoryName] = box

            # Create radiobutton
            isFirstBox = len(self.radioButtons) == 0
            self.categoryBox.addWidget(
                GroupBoxRadioButton(self, self.radioButtons, categoryName, box, selected=isFirstBox))
            if isFirstBox:
                self.groupBox.showWidget(self.groupBoxes.values()[0])
        else:
            box = self.groupBoxes[categoryName]

        # Add slider to groupbox
        self.modifiers[slider.modifier.fullName] = slider.modifier
        box.addWidget(slider)
        slider.enabledCondition = enabledCondition
        self.sliders.append(slider)
        # log.message(str(sliders.getValue()))

    def updateMacro(self):
        self.human.updateMacroModifiers()

    def getModifiers(self):
        return self.modifiers

    def onShow(self, event):
        gui3d.TaskView.onShow(self, event)

        # Only show macro statistics in status bar for Macro modeling task
        # (depends on the correct task name being defined)
        if self.showMacroStats:
            self.showMacroStatus()

        if G.app.getSetting('cameraAutoZoom'):
            self.setCamera()

        self.syncSliders()

    def syncSliders(self):
        for slider in self.sliders:
            slider.update()
            if slider.enabledCondition:
                enabled = getattr(slider.modifier.human, slider.enabledCondition)()
                slider.setEnabled(enabled)

    def onHide(self, event):
        super(Modifier1TaskView, self).onHide(event)

        if self.name == "Macro modelling":
            self.setStatus('')

    def onHumanChanged(self, event):
        # Update sliders to modifier values
        self.syncSliders()

        if event.change in ('reset', 'load', 'random'):
            self.updateMacro()

        if self.showMacroStats and self.isVisible():
            self.showMacroStatus()

    def loadHandler(self, human, values, strict):
        pass

    def saveHandler(self, human, file):
        pass

    def setCamera(self):
        if self.cameraFunc:
            f = getattr(G.app, self.cameraFunc)
            f()

    def showMacroStatus(self):
        human = G.app.selectedHuman

        if human.getGender() == 0.0:
            gender = G.app.getLanguageString('female')
        elif human.getGender() == 1.0:
            gender = G.app.getLanguageString('male')
        elif abs(human.getGender() - 0.5) < 0.01:
            gender = G.app.getLanguageString('neutral')
        else:
            gender = G.app.getLanguageString('%.2f%% female, %.2f%% male') % (
            (1.0 - human.getGender()) * 100, human.getGender() * 100)

        age = human.getAgeYears()
        muscle = (human.getMuscle() * 100.0)
        weight = (50 + (150 - 50) * human.getWeight())
        height = human.getHeightCm()
        if G.app.getSetting('units') == 'metric':
            units = 'cm'
        else:
            units = 'in'
            height *= 0.393700787

        self.setStatus([['Gender', ': %s '], ['Age', ': %d '], ['Muscle', ': %.2f%% '], ['Weight', ': %.2f%% '],
                        ['Height', ': %.2f %s']], gender, age, muscle, weight, height, units)

    def setStatus(self, format, *args):
        G.app.statusPersist(format, *args)


class GroupBoxRadioButton(gui.RadioButton):
    def __init__(self, task, group, label, groupBox, selected=False):
        super(GroupBoxRadioButton, self).__init__(group, label, selected)
        self.groupBox = groupBox
        self.task = task

    def onClicked(self, event):
        self.task.groupBox.showWidget(self.groupBox)
        # self.task.onSliderFocus(self.groupBox.children[0]) # TODO needed for measurement


def _getCamFunc(cameraName):
    if cameraName:
        if hasattr(gui3d.app, cameraName) and callable(getattr(gui3d.app, cameraName)):
            return cameraName

        return "set" + cameraName.upper()[0] + cameraName[1:]
    else:
        return None


def loadModifierTaskViews(filename, human, category, taskviewClass=None):
    """
    Create modifier task views from modifiersliders defined in slider definition
    file.
    """
    import json

    if not taskviewClass:
        taskviewClass = Modifier1TaskView

    data = json.load(open(filename, 'rb'), object_pairs_hook=OrderedDict)
    taskViews = []
    # Create task views
    for taskName, taskViewProps in data.items():
        sName = taskViewProps.get('saveName', None)
        label = taskViewProps.get('label', None)
        taskView = taskviewClass(category, taskName, label, sName)
        taskView.sortOrder = taskViewProps.get('sortOrder', None)
        taskView.showMacroStats = taskViewProps.get('showMacroStats', None)
        category.addTask(taskView)

        # Create sliders
        for sliderCategory, sliderDefs in taskViewProps['modifiers'].items():
            for sDef in sliderDefs:
                modifierName = sDef['mod']
                modifier = human.getModifier(modifierName)
                log.message(str(modifierName))
                log.message(str(modifier))
                label = sDef.get('label', None)
                camFunc = _getCamFunc(sDef.get('cam', None))
                slider = modifierslider.ModifierSlider(modifier, label=label, cameraView=camFunc)
                enabledCondition = sDef.get("enabledCondition", None)
                taskView.addSlider(sliderCategory, slider, enabledCondition)

        if taskView.saveName is not None:
            gui3d.app.addLoadHandler(taskView.saveName, taskView.loadHandler)
            gui3d.app.addSaveHandler(taskView.saveHandler)

        taskViews.append(taskView)

    return taskViews


def load(app):
    category = app.getCategory('Utilities')
    # taskview = category.addTask(AotuclassTaskView(category))
    loadModifierTaskViews(fileStartDir + '/data/MyAutoData/Mysliders.json', app.selectedHuman, category)


def unload(app):
    pass
