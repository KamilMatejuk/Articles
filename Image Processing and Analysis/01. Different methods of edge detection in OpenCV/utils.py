import cv2
import matplotlib.pyplot as plt


def read_rgb(name, show=True, rotate=False):
    image = cv2.imread(name)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if rotate: image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    if show: show_im(image)
    return image


def read_bw(name, show=True, rotate=False):
    image = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
    if rotate: image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    if show: show_im(image, 'grey')
    return image


def show_im(image, cmap=None, title=None, figsize=None):
    kwargs = {} if figsize is None else {'figsize': figsize}
    fig, ax = plt.subplots(frameon=False, **kwargs)
    kwargs = {}
    if cmap is not None: kwargs['cmap'] = cmap
    if cmap == 'grey': kwargs['cmap'] = plt.colormaps.get_cmap('Greys').reversed()
    ax.imshow(image, **kwargs)
    ax.axis('off')
    if title is not None: ax.set_title(title)
    fig.tight_layout()
    # plt.show()
    # return None