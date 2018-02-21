import numpy as np
from PIL import Image
import math


def with_white_bg(img):
    white_bg = Image.new(mode=img.mode, size=img.size, color='white')
    white_bg.paste(img, mask=img)
    return white_bg


def red(image):
    arr = np.asarray(image).copy()
    rgb = arr[:,:,1:3]
    arr[:,:,1:3][np.where(rgb == 255)] = 0
    red_rank = Image.fromarray(arr)
    return with_white_bg(red_rank)


def black(image):
    arr = np.asarray(image).copy()
    rgb = arr[:,:,0:3]
    arr[:,:,0:3][np.where(rgb == 255)] = 0
    black_rank = Image.fromarray(arr)
    return with_white_bg(black_rank)


def affine(img, angle, center, new_center, scale):
    angle = -angle/180.0*math.pi
    nx,ny = x,y = center
    sx=sy=1.0
    (nx,ny) = new_center
    (sx,sy) = scale
    cosine = math.cos(angle)
    sine = math.sin(angle)
    a = cosine/sx
    b = sine/sx
    c = x-nx*a-ny*b
    d = -sine/sy
    e = cosine/sy
    f = y-nx*d-ny*e
    
    fff = Image.new(img.mode, img.size, (255,)*len(img.mode))
    warped_img = img.transform(img.size, Image.AFFINE, (a,b,c,d,e,f))
    img = Image.composite(warped_img, fff, warped_img)
    
    return img