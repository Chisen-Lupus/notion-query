import requests, json, os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

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

def get_page_id(page): 
    page_url = page['url']
    page_id = page_url.split('/')[-1].split('-')[-1]
    # page_url = f'https://api.notion.com/v1/pages/{page_id}'
    return page_id