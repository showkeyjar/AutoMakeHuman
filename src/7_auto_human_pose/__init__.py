#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .auto_human_pose import PoseLibraryAotu1TaskView


def load(app):
    category = app.getCategory('Utilities')
    taskview = category.addTask(PoseLibraryAotu1TaskView(category))
    app.addLoadHandler('pose', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler, priority=6)


def unload(app):
    pass
