import numpy as np
from itertools import cycle, islice
from os import listdir, path
from os.path import isfile, join
from PIL import Image

import canvas


def warp(image, lvl):
    r = lambda v: v * (.5 - np.random.rand()) * lvl
    width, height = image.size
    
    angle = r(45)
    center = width/2 + r(width/4), height/2 + r(height/4)
    new_center = width/2 + r(width/4), height/2 + r(height/4)
    scale = 1 + r(.5), 1 + r(.5)
    
    return canvas.affine(image, angle, center, new_center, scale)


def as_array(img):
    arr = np.asarray(img, dtype=np.float32)
    arr_max = arr.max()
    norm_arr = abs(arr - arr_max) / arr_max
    return norm_arr


class Samples(object):
    def __init__(self, images_dir, mode='L', warp_lvl=.5, one_hot=True):
        self.images_dir = images_dir
        self.mode = mode
        self.warp_lvl = warp_lvl
        self.one_hot = one_hot
        
        samples = list(self.read_images(images_dir))
        self.images, self.labels = zip(*samples)
        
        self.vocabulary = sorted(list(set(self.labels)))
        self.labels = [self.vocabulary.index(lbl) for lbl in self.labels]
        
        if self.one_hot:
            one_hot = np.zeros((len(self.labels), len(self.vocabulary)))
            idx = np.arange(len(self.labels))
            one_hot[idx, self.labels] = 1
            self.labels = one_hot

            
    def read_images(self, images_dir):
        for name in listdir(images_dir):
            full_path = join(images_dir, name)
            if not isfile(full_path):
                continue

            label = path.splitext(path.basename(full_path))[0]
            image = Image.open(full_path)
            red_image = canvas.red(image)
            black_image = canvas.black(image)

            yield (red_image, label)
            yield (black_image, label)
    
    
    def preprocess(self, img, warp_lvl):
        warped_img = warp(img, warp_lvl).convert(self.mode)
        arr = as_array(warped_img)
        return arr

    
    def next_batch(self, count):
        idx = np.arange(len(self.images))
        idx = list(islice(cycle(idx), 0, count))
        np.random.shuffle(idx)
        X = np.stack([self.preprocess(self.images[i], self.warp_lvl) for i in idx])
        y = self.labels[idx]
        return X, y