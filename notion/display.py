import requests, json, os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def setup_matplotlib_inline():
    try:
        from IPython import get_ipython
        ipython = get_ipython()
        if ipython is not None:
            ipython.run_line_magic('matplotlib', 'inline')
            ipython.run_line_magic('config', "InlineBackend.figure_format = 'retina'")
    except ImportError:
        print("IPython is not installed. Please install it to use this feature.")

def display_single_image(path):
    # Open the image using Pillow
    img = Image.open(path)

    # Display the image
    plt.imshow(img)
    plt.axis('off')  # Hide axes
    plt.show()

def display_multiple_images(paths):
    img_count = len(paths)
    grid = int(np.ceil(np.sqrt(img_count)))
    fig, axs = plt.subplots(grid, grid)
    axs = axs.flat
    for i in range(len(axs)):
        if i<img_count:
            path = paths[i]
            img = Image.open(path)
            axs[i].imshow(img)
        axs[i].axis('off')  # Hide axes
    plt.tight_layout()
    plt.show()