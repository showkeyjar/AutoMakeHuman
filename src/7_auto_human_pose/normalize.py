# -*- coding: utf-8 -*-
import logging

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


HEIGHT = 90
WIDTH = 60


def _find_contours(image):
    result = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(result) == 3:
        _, contours, _ = result
    else:
        contours, _ = result
    return contours


def GetFinalContour(contour, num):
    del num
    if not contour:
        raise ValueError('No contours found in image')
    if len(contour) == 1:
        return contour[0]
    return np.concatenate(contour, axis=0)


def ReadImg(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img_gray, 100, 255, 0)
    return thresh


def GetMeans(thresh):
    contours = _find_contours(thresh)
    cnt = GetFinalContour(contours, len(contours))
    moments = cv2.moments(cnt)
    cx = int(moments['m10'] / moments['m00'])
    cy = int(moments['m01'] / moments['m00'])
    return cx, cy, cnt


def GetHeadMeans(imgH):
    contours = _find_contours(imgH)
    cnt = GetFinalContour(contours, len(contours))

    topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
    bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
    log.message("Topmost=%d bottommost=%d", topmost[1], bottommost[1])

    height1, width1 = imgH.shape[:2]
    head_height = max(int(height1 * 0.12), 1)
    thresh = imgH[topmost[1]:int(topmost[1] + head_height), 1:width1]

    contours_head = _find_contours(thresh)
    cnt1 = GetFinalContour(contours_head, len(contours_head))

    moments_head = cv2.moments(cnt1)
    moments_body = cv2.moments(cnt)

    cx = int(moments_head['m10'] / moments_head['m00'])
    cy = int(moments_body['m01'] / moments_body['m00'])
    return cx, cy, cnt


def GetNormalPic(imgm):
    img = ReadImg(imgm)
    img1 = imgm.copy()
    rows, cols = img.shape
    cx, _, cnt = GetHeadMeans(img)

    topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
    bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
    height = bottommost[1] - topmost[1]
    new_x = cx - height / 3.0
    new_width = height * 2.0 / 3.0
    matrix = np.float32([[1, 0, 0], [0, 1, 0]])

    if new_x + new_width > cols:
        delta_x = cols - (new_x + new_width)
        matrix[0][2] = float(delta_x)
        dst = cv2.warpAffine(img1, matrix, (cols, rows))
        person = dst[topmost[1]:bottommost[1], int(new_x + delta_x):cols]
    elif new_x < 0:
        matrix[0][2] = float(abs(new_x))
        dst = cv2.warpAffine(img1, matrix, (cols, rows))
        person = dst[topmost[1]:bottommost[1], 0:int(new_width)]
    else:
        dst = img1
        person = dst[topmost[1]:bottommost[1], int(new_x):int(new_x + new_width)]

    return cv2.resize(person, (WIDTH, HEIGHT))


def Normalize(im):
    return GetNormalPic(im)
