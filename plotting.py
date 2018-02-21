import matplotlib.pyplot as plt
import numpy as np

def stack_images(images, labels=None, num_cols=None, num_rows=None, cmap='gray'):
    if num_cols is None:
        num_cols = len(images)
    if num_rows is None:
        num_rows = len(images) / num_cols
    width, height = 2 * num_cols, 3 * num_rows
    fig = plt.figure(figsize=(width, height))
    
    items = list(enumerate(images))
    items = items[:int(num_rows*num_cols)]
    
    for i, image in items:
        data = np.asarray(image)

        ax = fig.add_subplot(num_rows, num_cols, i+1)

        ax.imshow(data, cmap=cmap, interpolation='none')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        if labels is not None:
            if len(labels) == len(images):
                label = labels[i]
            else:
                label = labels
            ax.text(0, 0, label, bbox={'facecolor':'white', 'pad':5}, fontdict={'size':14, 'weight':'bold'})