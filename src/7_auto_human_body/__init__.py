#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .auto_human_body import loadModifierTaskViews

make_human_path = 'D:/Python/human/makehuman/makehuman'
fileStartDir = make_human_path + '/plugins/7_auto_human_body'


def load(app):
    category = app.getCategory('Utilities')
    # taskview = category.addTask(AotuclassTaskView(category))
    loadModifierTaskViews(fileStartDir + '/data/MyAutoData/Mysliders.json', app.selectedHuman, category)


def unload(app):
    pass
