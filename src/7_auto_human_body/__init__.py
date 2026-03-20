#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from .auto_human_body import loadModifierTaskViews

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
SLIDER_CONFIG = os.path.join(PLUGIN_DIR, 'data', 'MyAutoData', 'Mysliders.json')


def load(app):
    category = app.getCategory('Utilities')
    loadModifierTaskViews(SLIDER_CONFIG, app.selectedHuman, category)


def unload(app):
    pass
