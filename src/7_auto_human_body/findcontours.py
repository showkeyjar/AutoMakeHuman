# -*- coding: utf-8 -*-
import logging
import os

import cv2
import numpy as np

try:
    import log  # type: ignore
except ImportError:  # pragma: no cover
    class _LogShim:
        @staticmethod
        def message(msg, *args):
            logging.getLogger(__name__).info(msg, *args)

    log = _LogShim()


DEBUG_WINDOWS = os.environ.get('AUTO_MAKEHUMAN_DEBUG_WINDOWS', '').lower() in {'1', 'true', 'yes'}


def _find_contours(image):
    result = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(result) == 3:
        _, contours, _ = result
    else:
        contours, _ = result
    return contours


def _merge_contours(contours):
    if not contours:
        raise ValueError('No contours found in image')
    if len(contours) == 1:
        return contours[0]
    return np.concatenate(contours, axis=0)


def FindContours1(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return _find_contours(gray)


def FindContours(OrigalIm):
    gray = cv2.cvtColor(OrigalIm, cv2.COLOR_BGR2GRAY)
    return _find_contours(gray)


def MatchContours(contour1, contour2):
    return cv2.matchShapes(contour1, contour2, 3, 0)


def GetFinalContour(contour, num):
    del num
    return _merge_contours(list(contour))


def CalDiff(img, img2):
    imgDiff = cv2.absdiff(img, img2)
    if DEBUG_WINDOWS:
        cv2.imshow("imgDiff", imgDiff)
        cv2.waitKey(1)
    height1, width1 = img.shape[:2]
    normal = 255 * height1 * width1
    total = imgDiff.sum() + 0.001
    avr = total / normal
    log.message("height= %d width=%d Normal=%f AVR=%f", height1, width1, normal, avr)
    return avr


def GetDeltValue(img, img2):
    contour1 = GetFinalContour(FindContours1(img), 0)
    contour2 = GetFinalContour(FindContours(img2), 0)
    return MatchContours(contour1, contour2)
